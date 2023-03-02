#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <sys/types.h>
#include <fcntl.h>
#include <sys/stat.h>
#include "libDisk.h"


int openDisk(char *filename, int nBytes) {
  	int fd = -1;
  	if(nBytes == 0){
    	fd = open(filename);
    }
  	else if (nbytes < 0){
      	return fd;
    }
  	else{
      	fd = open(filename);
        lseek(fd, 0, SEEK_SET);
        write(fd, '\0', BLOCKSIZE * nBytes);  
    }
  	return fd;
}

int readBlock(int disk, int bNum, void *block) {
  	if(bNum < 0){
    	return -1;
    }
	else if(lseek(disk, bNum * BLOCKSIZE,SEEK_SET) < 0){
    	return -1;
    }  
  	//lseek(disk, bNum * BLOCKSIZE, SEEK_SET);
  	read(disk, block, BLOCKSIZE);
  	return 0;
}

int writeBlock(int disk, int bNum, void *block) {
  	if(bNum < 0){
    	return -1;
    }
	else if(lseek(disk, bNum * BLOCKSIZE, SEEK_SET) < 0){
    	return -1;
    }
	//lseek(disk, bNum * BLOCKSIZE, SEEK_SET);
  	write(disk, block, BLOCKSIZE);
    return 0;
}

void closeDisk(int disk)
{
	if(disk < 0)
    {
      return -1;
    }
  	if(close(disk) == 1)
    {
      return -1;
    }
  	return 0;
}