EMAIL=$1
if [[ ! "$EMAIL" =~ ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$ ]]
then
    echo "You must supply your email address as the first argument"
    exit 1
fi

# Set user's email.
if grep -Fq "JOB_MAIL" ~/.bash_profile ; then
  echo "Email address environment variables present in .bash_profile"
else
  echo "Adding email address to environment variables in .bash_profile"
  echo "export JOB_MAIL=$EMAIL" >> ~/.bash_profile
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
echo "COULOMB_MODULES_DIR=~/projects/def-coulomb/modules" >> ~/.coulomb_addons
echo 'if [ -d "$COULOMB_MODULES_DIR" ]; then' >> ~/.coulomb_addons
echo '  module use $COULOMB_MODULES_DIR' >> ~/.coulomb_addons
echo 'fi' >> ~/.coulomb_addons
echo "" >> ~/.coulomb_addons
