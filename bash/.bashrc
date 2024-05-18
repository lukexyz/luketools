# ===== open =====
# nano ~/.bashrc
# source ~/.bashrc

commit () { git commit -am "${1}"; git push; }

# luke ~./bashrc
eval "$(oh-my-posh --init --shell bash --config ~/.poshthemes/powerlevel10k_modern.omp.json)"

# sudo apt-get install neofetch
neofetch --ascii_distro macosx     
# neofetch --ascii_distro ubuntu_small  

alias cls="clear"
alias ls="ls -l"
alias dir="ls -l"

# https://news.ycombinator.com/item?id=32998960
alias brownnoise='play -n synth brownnoise synth pinknoise mix synth sine amod 0.3 10'

cd /mnt/d/python
echo ''
ls
