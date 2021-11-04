
# luke ~./bashrc
eval "$(oh-my-posh --init --shell bash --config ~/.poshthemes/powerlevel10k_modern.omp.json)"

# sudo apt-get install neofetch
neofetch --ascii_distro ubuntu_small

cd /mnt/c/python
ls -l
echo ''
alias cls="clear"




# Look up the proper conda init yourself, looks a little something like this
# ============================================================================

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/mnt/c/python/wsl/conda/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/mnt/c/python/wsl/conda/etc/profile.d/conda.sh" ]; then
        . "/mnt/c/python/wsl/conda/etc/profile.d/conda.sh"
    else
        export PATH="/mnt/c/python/wsl/conda/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

# ============================================================================
