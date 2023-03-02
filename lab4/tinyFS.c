#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <sys/types.h>
#include <fcntl.h>
#include <sys/stat.h>
#include "libDisk.h"
#include "tinyFS.h"

char *mounted = NULL;

TableEntry *table[100];
int tablePosition = 0;

int tfs_mkfs(char *filename, int nBytes){
  	void *block;
  	Block *super, *dummy;
  	SpecialInode *specialInode;
  	int input = (openDisk(filename, nBytes)
             
	if (input == -1)) {
    	return -1;
    }
  	super->magic = 0x5A;
  	super->rootInode = 1 	//??
    super->freeBlockNum = 2 	//??
      
    
    writeBlock(input, 0, super);
  	for(i=1;i<(DEFAULT_DISK_SIZE/BLOCKSIZE);i++){
		writeBlock(input, i, dummy);
    }
  
  
  	return 0;
}

int tfs_mount(char *filename){
  	if(mounted != NULL){
		tfs_unmount();
    }
  	if(openDisk(filename, 0) == -1) {
      	return -1;    	// maybe new error code?
    }
  	
  	mounted = filename;
}

int tfs_unmount(void){
  	if(mounted = NULL){
    	return -1;
    }
  	if(tablePosition){				//check for empty table
      	return -1;
    }
  	mounted = NULL;
  	//free();							//free the table
  	//free();							//free superblock
  	//free();							//free blocks
  	return 0;
}

fileDescriptor tfs_open(char *name){
  	int fd = -1;
  	void block[BLOCKSIZE];
  	char *curName;
  	flag = 0;
    
    fd = openDisk(mounted, 0);
  	if(strlen(name) > MAXLENGTH){
      	free(name);
      	return -1
    }
  
  

  	TableEntry *entry = malloc(sizeof(TableEntry));
  	entry->filename = name;
  	entry->fd = fd;
	table[tablePosition] = &entry;
  	tablePosition++;
  	return fd;
}

int tfs_close(fileDescriptor FD){
  	int flag = 0;
  	if(FD < 0 || mounted == NULL){
		return -1;	//error code
    }
  	/*while(entry->fd != FD && entry->next != NULL){
      	entry = entry->next;
    }
  	if((entry->next == NULL) && entry->fd != FD)
      	return -2	//error code*/
    
    int i;
  	for (i = 0; i < 100; i++){	//need to set all values to NULL in beginning
      	if ((table[i] != NULL) && (table[i]->fd == FD)){
          	free(table[i]);
          	flag = 1;
          	table[i] = NULL;
          	break;
        }
    }
  	if(flag == 1)
  		close(FD);
  	else
      	return -3;	//error code
  	return 0;
}

int tfs_write(fileDescriptor FD, char *buffer, int size){	//might need to add to this function, like adding new inodes
	if(write(FD, buffer, size) < 0){
      	return -1;		// error code
    }
  	fseek(FD, 0, SEEK_SET);
  	return 0;
}

int tfs_delete(fileDescriptor FD){
  	TableEntry *entry;
  	char *curName;
  	char* dummyFilename;
  	int flag, blockNumber = 0;
  	void *block;  //these needs to be BLCOKSIZE full of NULL

  	for(i=0;i<100;i++){
      	if ((table[i] != NULL) && (table[i]->fd == FD)){
          	free(table[i]);
          	entry = table[i];
          	flag = 1;
        }
    }

    if(flag == 0){
      	return -4;	//filename was not in the Resource Table
    }

    flag = 0;
    dummyFilename = entry->filename;

    for(i = 0; i < DEFAULT_DISK_SIZE; i+=BLOCKSIZE){
      	readBlock(fd, i, block);
      	if(block[1] == 2){ 		//2 = inode
          	curName = block + 10;
          	if(strcmp(name, curName) == 0){
              	flag = 1;
              	blockNumber = i / BLOCKSIZE;
              	break;
            }
        }
    }

    writeBlock(fd, blockNumber, block);
    return 0;
}

int tfs_readByte(fileDescriptor FD, char *buffer){
  	fseek(FD, 0, SEEK_CUR);
  	if (fread(buffer, sizeof(char), 1, FD) < 0){
      	return -1;
    }
  	fseek(FD, 1, SEEK_CUR);
  	return 0;
}

int tfs_seek(fileDescriptor FD, int offset){
  	char *curName;
  	int blockNumber, flag = 0;
  	void *block;
	if(fseek(FD, offset, SEEK_CUR) < 0){			//variable of number of where the file disk is at, checking if valid
      return -1;
    }
  	if(FD < 0 || < 0){									//needs a reference to address 				
      return -1;
    }
  	for(i = 0; i < DEFAULT_DISK_SIZE; i+=BLOCKSIZE){
      	readBlock(fd, i, block);
      	if(block[1] == 2){ 		//2 = inode
          	curName = block + 10;
          	if(strcmp(name, curName) == 0){
              	flag = 1;
              	blockNumber = i / BLOCKSIZE;
              	break;
            }
        }
    }

  	if(flag != 1){
      	return -4;	//error code
    }
  	readBlock(FD, blockNumber, block);
  	block[6] = offset;
  	return 0;
}


/* Unimplemented
 * Directory listing and renaming
 * ===========================================================
	int tfs_rename(char *old, char* new){
    	int bufferpointer
        char *name
        
      	check mounted
        update blocks and superblocks
        check if the name of the file is within bounds
        check if new name is within bounds
        
        search inodes with the pointer name
        check if the file is readonly
      	copy the new name to the block        
    }
    
    
    int tfs_readdir(){
    	check if mounted
        update blocks and superblock
        
        check the superblockkk for the byte of the inode
        print the result
    }


    Timestamp
    ====================================================
    
  	char* tfs_stat(fileDescriptor FD){
      timestamp *ptr
      inode *ptr
      fd *ptr
      
      Error checks for valid FD
      check if timestamp exists in the buffer
      if not allocate memory for timestamp to the buffer
      
      have the fd *ptr point to the table[FD]
      have the inode equal the fd inode 
      timestamp with localtime() to the inode's time variable
      copy the timestamp to the timestamp buffer memory
  	}

	ReadOnly and writeByte
    =======================================================================
    int tfs_makeRO(char *name){
    	int buffer
        char *tail
        
        check mount and update blocks
        
        check the name length if valid
        search inode for the block at the tail of the list
        set the block after tail to 1
        write to the blocktable the new block
        
    }
    
    int tfs_makeRW(char *name){
    	int buffer
        char *tail
        
        check mount and update
        
    	check the name length if valid
        search inode for the block at the tail of the list
        set the block after tail to 1
        write to the blocktable the new block
    
    }
    
    int tfs_writeByte(fileDescriptor FD, unsigned char data){
    	int buffer
        
        error checks
        check if the fd is within bounds of the file
        have the block starting at the buffer of the fd + the datasize = the data
  		increment the file pointer of the block
    }
*/