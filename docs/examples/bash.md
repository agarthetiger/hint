# ssh

* `ssh-keygen -o -a 100 -t ed25519 -f ~/.ssh/id_ed25519 -C "<user@host>"` Generate a strong ssh key
* `eval $(ssh-agent -s)` Start the ssh agent
* `ssh-keygen -R <hostname_or_ip>` Remove a host fingerprint from the known hosts 

# curl

* `curl -s "https://pypi.org/pypi/<package_name>>/json" | jq  -r '.releases | keys | .[]' | sort -V` Get all available versions of a package from pypi.org
