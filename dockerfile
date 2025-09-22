# Start from the official Jenkins Long-Term Support (LTS) image.
FROM jenkins/jenkins:lts

# Switch to the root user to gain the necessary permissions to install software.
# The default 'jenkins' user does not have these privileges.
USER root

# Update the package lists and install Python 3 and its package manager, pip.
# The '-y' flag automatically confirms the installation.
RUN apt-get update && apt-get install -y python3 python3-pip

# Switch back to the 'jenkins' user. This is a security best practice
# to avoid running the Jenkins service with administrator privileges.
USER jenkins