if [ "$1" == "clean" ] ; then
    echo "Removing changes made to .bash_profile"
    INDEX=$(grep -n "alias sbatch=" ~/.bash_profile | cut -d: -f1)
    sed -i "$((INDEX)),$((INDEX+1))d" ~/.bash_profile
    INDEX=$(grep -n "source .coulomb_modules" ~/.bash_profile | cut -d: -f1)
    sed -i "$((INDEX-1)),$((INDEX+2))d" ~/.bash_profile
    if [ -f ~/.coulomb_addons ] ; then
        rm ~/.coulomb_addons
    fi
    exit 0
fi

EMAIL=$1
if [[ ! "$EMAIL" =~ ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$ ]] ; then
    echo "You must supply your email address as the first argument"
    exit 1
fi

# Set user's email.
if grep -Fq "export JOB_MAIL=" ~/.bash_profile ; then
    echo "Replacing email address environment variables present in .bash_profile"
    sed -i -E "s/export JOB_MAIL=.+/export JOB_MAIL=$EMAIL/" ~/.bash_profile
else
    echo "Adding email address to environment variables in .bash_profile"
    echo "export JOB_MAIL=$EMAIL" >> ~/.bash_profile
    echo "" >> ~/.bash_profile
fi

# Make sbatch send mail to user by default.
if grep -Fq "alias sbatch=" ~/.bash_profile ; then
    sed -i -E "s/alias sbatch=.+/alias sbatch='sbatch --mail-type=ALL --mail-user=\$JOB_MAIL'/" ~/.bash_profile
else
    echo "Adding email notification for sbatch"
    echo "alias sbatch='sbatch --mail-type=ALL --mail-user=\$JOB_MAIL'" >> ~/.bash_profile
    echo "" >> ~/.bash_profile
fi

# Remove direct configuration of coulomb modules, if present.
if grep -Fq "COULOMB_MODULES_DIR=" ~/.bash_profile ; then
    echo "Removing coulomb modules from .bash_profile"
    INDEX=$(grep -n "COULOMB_MODULES_DIR=" ~/.bash_profile | cut -d: -f1)
    sed -i "$((INDEX-1)),$((INDEX+4))d" ~/.bash_profile
fi

# Source .coulomb_addons file on login.
if ! grep -Fq "source .coulomb_addons" ~/.bash_profile ; then
    echo "Adding coulomb addons"
    echo 'if [ -f .coulomb_addons ]; then' >> ~/.bash_profile
    echo '  source .coulomb_addons' >> ~/.bash_profile
    echo 'fi' >> ~/.bash_profile
    echo "" >> ~/.bash_profile
fi

# Create .coulomb_addons file to alow loading of coulomb modules.
if [ -f ~/.coulomb_addons ] ; then
    rm ~/.coulomb_addons
fi
echo "## Coulombe Lab Modules ##" >> ~/.coulomb_addons
echo "MODULES_DIR=~/projects/def-coulomb/modules" >> ~/.coulomb_addons
echo 'if [ -d "$MODULES_DIR" ]; then' >> ~/.coulomb_addons
echo '  module use $MODULES_DIR' >> ~/.coulomb_addons
echo 'fi' >> ~/.coulomb_addons
echo "" >> ~/.coulomb_addons
