#include "lwp.h"
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

lwp_context lwp_ptable[LWP_PROC_LIMIT];     // process table
int lwp_procs = 0;                          // number of current libraries
int lwp_running;                            // lwp that is running
schedfun lwpSched = NULL;                   // current schedule
void * lwpSP;                               // initial pointer
unsigned long nextPID = 0;                   // next pid



int new_lwp(lwpfun function, void * arguement, size_t stacksize)
{
    if(lwp_procs == LWP_PROC_LIMIT)
    {
        return -1;
    }
    ptr_int_t * stack_ptr;
    ptr_int_t * base_ptr;

    lwp_running = lwp procs++;
    lwp_ptable[lwp_running].pid = nextPID++;
    lwp_ptable[lwp_running].stacksize = stacksize;
    lwp_ptable[lwp_running].stack = malloc(stacksize * sizeof(ptr_int_t));
    stack_ptr = lwp_ptable[lwp_running].stack + (stacksize * sizeof(ptr_int_t));    //goes to current lwp stack
    base_ptr = stack_ptr;

    *stack_ptr = (ptr_int_t)arguement;  //args pushed
    stack_ptr--;
    *stack_ptr = (ptr_int_t)lwp_exit;   //exit pushed
    stack_ptr--;
    *stack_ptr = (ptr_int_t)function;   //return pushed
    stack_ptr--;

    *stack_ptr = 0xDEADC0DE;            //bogus ptr
    base_ptr = stack_ptr;
    stack_ptr -= 7;
    *stack_ptr (ptr_int_t)base_ptr;

    lwp_ptable[lwp_running].sp = stack_ptr;

    return lwp_running;


}


int lwp_getpid()
{
    return (int)lwp_ptable[lwp_running].pid;
    // if(lwp_running > -1)
    // {
    //     return lwp_ptable[lwp_running].pid;
    // }
    // else
    // {
    //     return NULL;         // wasnt quite working
    // }
}

void lwp_yield()
{
    SAVE_STATE();       //save current
    GetSP(lwp_ptable[lwp_running].sp);  //save sp

    if(lwpSched == NULL)
    {
        lwp_running++;
        if(lwp_running == lwp_procs)
        {
            lwp_running = 0;
        }
        else
        {
            lwp_running = lwpSched();
        }

        SetSP(lwp_ptable[lwp_running].sp);
        RESTORE_STATE();
    }

    SetSP(lwp_ptable[lwp_running].sp);
    RESTORE_STATE();


}

void lwp_exit()
{
    free(lwp_ptable[lwp_running].stack);      //free sp

    int i = lwp_running + 1;            //shift process up
    for(i; i < lwp_procs; i++)
    {
        lwp_ptable[i-1] = lwp_ptable[i];
    }
    lwp_procs--;

    if(lwp_procs == 0)
    {
        lwp_stop();             //if no more threads
    }
    else
    {
        if(lwpSched == NULL)        //round robin
        {
            lwp_running = 0;
        }
        else
        {
            lwp_running = sched_fun();
        }
    }
    SetSP(lwp_ptable[lwp_running].sp);
    RESTORE_STATE();
}

void lwp_start()
{
    if(lwp_procs == 0)
        return;

    SAVE_STATE();               //context save
    GetSP(lwpSP);               //SP save 

    if(lwpSched == NULL)        //round robin
    {
        lwp_running = 0;
    }
    else{
        lwp_running = lwpSched();
    }
    SetSP(lwp_ptable[lwp_running].sp);
    RESTORE_STATE();
}

void lwp_stop()
{
    SAVE_STATE();       // save current state
    SetSP(lwpSP);       // reset stackpointer
    RESTORE_STATE();    // continue from saved
}

void lwp_set_scheduler(schedfun sched)
{
    // if(!lwpSched)
    // {
    //     lwpSched = malloc(sizeof(schedfun));
    // }
    lwpSched = sched;
}

