char Dname[] = "demo.d";
int fd;

if(tfs_mkfs(Dname, DEFAULT_DISK_SIZE) != 0)
  	return -10
if(tfs_mount(Dname) < 0)
	return -11
if(tfs_unmount() != 0)
  	return -12
if(tfs_mount(Dname) < 0)
  	return -11
if(tfs_open("test.txt") < 0)
  	return -13
if(tfs_close("test.txt") != 0)
  	return -14
if((fd = tfs_open("rwTest.txt")) < 0)
  	return -13
if(tfs_write(fd, "Hi there", 9))
  	return -15
if(tfs_seek(fd, 1) != 0)
  	return -16