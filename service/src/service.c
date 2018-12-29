#include <assert.h>
#include <stdio.h>
#include <string.h>
#include <dirent.h>
#include <sys/time.h>
#include <openssl/pem.h>
#include <openssl/ssl.h>
#include <openssl/rsa.h>
#include <openssl/evp.h>
#include <openssl/bio.h>
#include <openssl/err.h>
#include <openssl/bn.h>
#include <openssl/md5.h>
#include <openssl/crypto.h>
#define PUBLICKEYLENGTH 500
#define KEY_DIR "/keys"
#define FLAG_DIR "/flags"
#define DEBUG 0
#define printfd(fmt, ...) \
            do { if (DEBUG) fprintf(stderr, fmt, __VA_ARGS__); } while (0)


void printbin(unsigned char *x, int n){
    while(n--)  printf("%02X", *x++);
    printf("\n");
}

int public_encrypt(unsigned char * data, int data_len, RSA* rsa, unsigned char *encrypted) {
    return RSA_public_encrypt(data_len, data, encrypted, rsa, RSA_PKCS1_PADDING);
}

RSA *read_privatekey(int iteration){
    RSA *rsa= NULL;
    FILE *fp;
    char filename[30];

    if (iteration == -1)
        sprintf(filename, "%s/0.pem", KEY_DIR);
    else
        sprintf(filename, "%s/%d.pem", KEY_DIR, iteration);
    // puts(filename);
    fp = fopen(filename, "r");
    rsa = PEM_read_RSAPrivateKey(fp, &rsa, NULL, NULL);
    fclose(fp);
    if (rsa == NULL){
        printf( "Failed to create RSA");
        exit(0);
    }
    return rsa;
}

void send_publickey(int i){
    FILE *f;
    char filename[30], keystring[PUBLICKEYLENGTH];
    size_t newlen;
    sprintf(filename, "%s/%d.pub", KEY_DIR, i);
    f = fopen(filename, "r");
    newlen = fread(keystring, sizeof(char), PUBLICKEYLENGTH, f);
    keystring[newlen] = '\0';
    printf("%s\n", keystring);
    fclose(f);
}


void readFlagString(char* dst, int iteration){
    FILE *fp;
    char filename[30];
    int read;
    size_t len;
    sprintf(filename, "%s/%d", FLAG_DIR, iteration);
    fp = fopen(filename, "r");
    read = getline(&dst, &len, fp);
    fclose(fp);
    if (read == -1) exit(1);
    else dst[read - 1] = '\0';
}

const BIGNUM *BN_lowerhalf(const BIGNUM *d){
    BIGNUM *l = BN_dup(d);
    int len_bits = BN_num_bits(d);
    int start_bits = len_bits / 2 + 1;
    for(int i = 0; i < len_bits - start_bits; i++)
        BN_clear_bit(l, start_bits + i);
    return l;
}


const BIGNUM *get_hint(RSA *rsa){
    const BIGNUM *d = NULL, *low_d = NULL;

    RSA_get0_key(rsa, NULL, NULL, &d);
    low_d = BN_lowerhalf(d);
    // RSA_get0_key(rsa, &n, &e, &d);
    // printfd("n: %s\ne: %s\nd: %s\n", BN_bn2hex(n), BN_bn2hex(e), BN_bn2hex(d));
    // new_d_bits = BN_bn2binstr(new_d);
    // int len_bits = 0;
    // printfd("Bit length of d: %d\n", len_bits);
    // printfd("new d in bits: %s\n", new_d_bits);
    // printf("Hint: (%s, %ld)\n", &new_d_bits[len_bits - len_bits / 2], len_bits / 2);

    // Print the lower [len_bits/2] bits
    printf("Hint: %s, %d\n", BN_bn2hex(low_d), BN_num_bits(d) / 2 + 1);

    return low_d;
}

const BIGNUM *get_d(RSA *rsa){
    const BIGNUM *d = NULL;
    RSA_get0_key(rsa, NULL, NULL, &d);
    return d;
}

char *BN_bn2bytes(const BIGNUM *n){
    char *res = NULL;
    res = malloc(BN_num_bytes(n));
    BN_bn2bin(n, res);
    return res;
}

char *get_input(){
    ssize_t read;
    char *line = NULL;
    size_t len;

    if ((read = getline(&line, &len, stdin)) && (read > 0)) {
        line[read - 1] = '\0';
        return line;
    } else {
        printf("Read Input Error\n");
        return NULL;
    }
}


const BIGNUM *work(int iteration, const BIGNUM *old_d, int len_flag){
    const BIGNUM *new_d = NULL;
    const BIGNUM *low_new_d = NULL;
    char *old_bytes, *new_bytes, *input;
    RSA *new_rsa;
    int len_old_bytes, len_new_bytes;
    unsigned char *digest = NULL, *bytes = NULL, *encrypted = NULL;
    unsigned char plainText[MD5_DIGEST_LENGTH] = {}, flagText[MD5_DIGEST_LENGTH] = {};
    int key_index;

    // shuffle the key to be used;
    key_index = rand() % len_flag;
    // send public key
    send_publickey(key_index);

    // read new private key
    new_rsa = read_privatekey(key_index);

    // print hint, which is the lower half of the private key
    low_new_d = get_hint(new_rsa);

    // Read flag string from file
    readFlagString(flagText, iteration);

    // Get the digest
    // digest = md5.digest(old bytes || low_new_d bytes)
    old_bytes = BN_bn2bytes(old_d);
    len_old_bytes = BN_num_bytes(old_d);
    new_bytes = BN_bn2bytes(low_new_d);
    len_new_bytes = BN_num_bytes(low_new_d);
    bytes = malloc(len_old_bytes + len_new_bytes);
    memcpy(bytes, old_bytes, len_old_bytes);
    memcpy(bytes + len_old_bytes, new_bytes, len_new_bytes);
    digest = MD5((const unsigned char*)bytes, len_old_bytes + len_new_bytes, NULL);
    printf("Digest: ");
    printbin(digest, MD5_DIGEST_LENGTH);

    // plainText = flagText ^ digest
    assert(strlen(flagText) <= MD5_DIGEST_LENGTH);

    for (int i = 0; i < MD5_DIGEST_LENGTH; i++)
        if (i < strlen(flagText)) plainText[i] = flagText[i] ^ digest[i];
        else plainText[i] = ' ' ^ digest[i];

    //printfd("\nPlainText: ");
    //printbin(plainText, MD5_DIGEST_LENGTH);
    //printfd("\n");
    // Encrypt
    encrypted = malloc(RSA_size(new_rsa));
    int encrypted_length = public_encrypt(plainText,
                                          MD5_DIGEST_LENGTH,
                                          new_rsa,
                                          encrypted);
    // send
    printf("Encrypted Msg: ");
    printbin(encrypted, encrypted_length);
    printf("Input a string:\n");
    fflush(stdout);

    // receive input
    input = get_input();
    if (input && strstr(input, flagText))
        return get_d(new_rsa);
    else
        return NULL;
}

const BIGNUM *init(int len_flag){
    RSA *rsa = NULL;
    const BIGNUM *n = NULL;
    // Initialize the randomization of reading a privite key
    time_t t;
    srand((unsigned) time(&t));

    // Currently we set the seed as the n of the default key
    rsa = read_privatekey(-1);
    RSA_get0_key(rsa, &n, NULL, NULL);
    printf("Seed: %s\n", BN_bn2hex(n));
    return n;
}

int get_flag_length(){
    int file_count = 0;
    DIR * dirp;
    struct dirent * entry;
    dirp = opendir(FLAG_DIR);
    while ((entry = readdir(dirp)) != NULL)
        if (entry->d_type == DT_REG) /* If the entry is a regular file */
            file_count++;
    closedir(dirp);
    return file_count;
}

int main(){
  const BIGNUM *old_d = NULL, *new_d = NULL;
  int len_flag = 0;

  len_flag = get_flag_length();

  old_d = init(len_flag);
  for(int i = 0; i < len_flag; i++){
    new_d = work(i, old_d, len_flag);
    if (new_d == NULL)
        exit(1);
    else {
        old_d = new_d;
        if (i == len_flag - 1)
            printf("Yes, and now you know the flag\n");
        else
            printf("Yes, continue\n");
        fflush(stdout);
    }
  }
  return 0;
}
