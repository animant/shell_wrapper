# What is shell_wrapper
The tool is applied to command line interactive applications (like as debuggers and shells) and provides command history feature.
For example, jdb debugger doesn't provide command history and cursor moving. Using this tool, you obtain just simple useful command line.

# How to use

There are two ways to use the wrapper:

1) `python shell_wrapper.py -cmd <target application> [-opt "options"]`

    Example:

    `python shell_wrapper.py -cmd bash"`
    
    `python shell_wrapper.py -cmd jdb -opt "-attach 127.0.0.1:1234"`

2) 'Busybox'-like usage style (via symbolic links)

    Example:
    
    `ln -s shell_wrapper.py gdb.py`

    `python gdb.py ./executable.out`
