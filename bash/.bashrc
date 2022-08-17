
commit () { git commit -am "${1}"; git push; }

# luke ~./bashrc
eval "$(oh-my-posh --init --shell bash --config ~/.poshthemes/powerlevel10k_modern.omp.json)"

# sudo apt-get install neofetch
neofetch --ascii_distro ubuntu_small


alias cls="clear"
alias ls="ls -l"
alias dir="ls -l"

cd /mnt/d/python
echo ''
ls

