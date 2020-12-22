#include <iostream>
#include <fstream>
#include <cstdlib>
#include <sys/types.h>
#include <unistd.h>
#include <sys/resource.h>
#include <sys/time.h>
#include <sys/wait.h>
#include <cstdio>
#include <fcntl.h>
#include <string>
constexpr int UNDECIDE = 0;
constexpr int TLE = 2;
constexpr int MLE = 3;
constexpr int RE = 4;
constexpr int OK = 0;
constexpr int NOTOK = 1;
// timelimit is second
// memorylimit is kb
void setProcessLimit(rlim_t timelimit, rlim_t memory_limit)
{
    rlimit Time;
    Time.rlim_cur = timelimit;
    Time.rlim_max = timelimit + 1;
    /* set the time_limit (second)*/
    setrlimit(RLIMIT_CPU, &Time);

    rlimit Memory{.rlim_cur = memory_limit * 1024, .rlim_max = memory_limit * 1024 + 1024};
    /* set the memory_limit (b)*/
    setrlimit(RLIMIT_DATA, &Memory);
    // This steps only limit the system time
    itimerval empty{
        timeval{0, 0}, // it_interval
        timeval{0, 0}  // it_value
    };
    itimerval real{
        timeval{.tv_sec = 1, .tv_usec = 0},            // it_interval
        timeval{.tv_sec = timelimit * 2, .tv_usec = 0} // it_value
    };
    setitimer(ITIMER_REAL, &real, &empty);
    itimerval prof{
        timeval{.tv_sec = 0, .tv_usec = 0},            // it_interval
        timeval{.tv_sec = timelimit * 2, .tv_usec = 0} // it_value
    };
    setitimer(ITIMER_PROF, &prof, &empty);
    itimerval itimerval_virtual{
        timeval{.tv_sec = 0, .tv_usec = 0},            // it_interval
        timeval{.tv_sec = timelimit * 2, .tv_usec = 0} // it_value
    };
    setitimer(ITIMER_VIRTUAL, &itimerval_virtual, &empty);
}

struct result
{
    int status;
    int timeUsed;
    int memoryUsed;
};
void monitor(pid_t pid, int timeLimit, int memoryLimit, struct result *rest)
{
    auto outputOk = [](std::string path, int value) {
        std::ofstream outfile;
        outfile.open(path.c_str());
        outfile << value << std::endl;
        outfile.close();
    };
    int status;
    struct rusage ru;
    int runState = wait4(pid, &status, 0, &ru);
    if (runState == -1)
    {
        printf("wait4 failure");
    }
    rest->timeUsed = (ru.ru_utime.tv_sec * 1000 +
                      ru.ru_utime.tv_usec / 1000 +
                      ru.ru_stime.tv_sec * 1000 +
                      ru.ru_stime.tv_usec / 1000);
    outputOk("ruutime_tv_sec", ru.ru_utime.tv_sec * 1000);
    outputOk("ruutime_tv_usec", ru.ru_utime.tv_usec / 1000);
    outputOk("rustime_tv_sec", ru.ru_stime.tv_sec * 1000);
    outputOk("rustime_tv_usec", ru.ru_stime.tv_usec / 1000);
    rest->memoryUsed = ru.ru_maxrss;
    rest->status = UNDECIDE;
    if (WIFSIGNALED(status))
    {
        std::cout << WTERMSIG(status) << std::endl;
        std::cout << rest->timeUsed << " " << timeLimit * 1000 << '\n';
        std::cout << rest->memoryUsed << " " << memoryLimit << '\n';
        outputOk("./wtermsig", WTERMSIG(status));
        switch (WTERMSIG(status))
        {
        case SIGSEGV:
        {
            if (rest->memoryUsed > memoryLimit * 0.95)
            {
                rest->status = MLE;
                std::cout << "memoty out size 1" << std::endl;
            }
            else
            {
                std::cout << "Re 1" << std::endl;
                rest->status = RE;
            }
            break;
        }
        case SIGALRM:
        case SIGVTALRM:
        case SIGXCPU:
        case SIGPROF:
        {
            rest->status = TLE;
            break;
        }
        case SIGKILL:
        {
            if (rest->timeUsed > timeLimit * 900)
            {
                rest->status = TLE;
            }
            else if (rest->memoryUsed > memoryLimit * 0.95)
            {
                std::cout << "memoty out size 1.5" << std::endl;
                rest->status = MLE;
            }
        }
        }
        outputOk("./state", rest->status);
    }
    else
    {
        if (rest->timeUsed > timeLimit * 900)
        {
            rest->status = TLE;
            outputOk("./state", TLE);
        }
        else if (rest->memoryUsed > memoryLimit * 0.95)
        {
            std::cout << "memoty out size 2" << std::endl;
            rest->status = MLE;
            outputOk("./state", MLE);
        }
        else
        {
            outputOk("./state", OK);
        }
    }
    outputOk("./cputime", rest->timeUsed);
    outputOk("./memoryCost", rest->memoryUsed);
}

int main(int argc, char *argv[])
{
    if (argc < 3)
    {
        return 0;
    }
    auto timeLimit = atoi(argv[1]);
    auto memotyLimit = atoi(argv[2]);
    std::cout << timeLimit << " " << memotyLimit << std::endl;
    int pid = vfork();
    if (pid < 0)
    {
        //std::cout << "Error during fork" << '\n';
    }
    else if (pid == 0)
    {
        //std::cout << "This is child, pid is " << getpid() << '\n';
        int newstdin = open("./searchTable.sql", O_RDWR | O_CREAT, 0644);
        int newstdout = open("./result.log", O_RDWR | O_CREAT, 0644);
        setProcessLimit(timeLimit, memotyLimit);
        if (newstdout != -1 && newstdin != -1)
        {
            dup2(newstdout, fileno(stdout));
            dup2(newstdin, fileno(stdin));
            char *commands[] = {"mysql", "--defaults-file=/tmp/.mysql", argv[3], nullptr};
            int returnEd = execvp(commands[0], commands);
            if (returnEd == -1)
            {
                returnEd = -2;
            }
            else
            {
                std::cout << "Wrong" << std::endl;
            }
            close(newstdin);
            close(newstdout);
        }
        else
        {
            printf("====== Failed to open file! =====\n");
        }
        _exit(0);
    }
    else
    {
        result rest{0, 0, 0};
        monitor(pid, timeLimit, memotyLimit, &rest);
        //std::cout << "This is Father, pid is" << getpid() << '\n';
        exit(0);
    }
}