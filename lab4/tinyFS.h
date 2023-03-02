#ifndef TINYFS_H
#define TINYFS_H

#define BLOCKSIZE 256
#define DEFAULT_DISK_SIZE 10240
#define MAGIC_NUMBER 0x5A

#define DEFAULT_DISK_NAME "tinyFSDisk"
typedef int fileDescriptor;

typedef struct Pair{
  	char name[9];
  	char inodeNum;
} Pair;

typedef struct Superblock{
  	unsigned char magic;
    unsigned char rootInode;
    unsigned char freeBlockNum;
} Superblock;

typedef struct SpecialInode{
  	Pair *pairList[];
}

typedef struct Inode{
  	unsigned char number;
  	unsigned char filename;
  	unsigned char size;
} Inode;

typedef struct Freeblock{
	// *nextBlock;
} Freeblock;

typedef struct TableEntry{
  	
} TableEntry;

int tfs_mkfs(char *filename, int nBytes);
int tfs_mount(char *filename);
int tfs_unmount(void);
fileDescriptor tfs_open(char *name);
int tfs_close(fileDescriptor FD);
int tfs_write(fileDescriptor FD, char *buffer, int size);
int tfs_delete(fileDescriptor FD);
int tfs_readByte(fileDescriptor FD, char *buffer);
int tfs_seek(fileDescriptor FD, int offset);
  
#endif