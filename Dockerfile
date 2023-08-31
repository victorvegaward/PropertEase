# Starting with a Node image
FROM node:16

# Update the system
RUN apt-get update && apt-get upgrade -y

# Install Ruby dependencies
RUN apt-get install -y ruby-full build-essential zlib1g-dev

# Set up environment for ruby installation
ENV GEM_HOME /usr/local/bundle
ENV PATH $GEM_HOME/bin:$GEM_HOME/gems/bin:$PATH

# Install CocoaPods
RUN gem install cocoapods

# Install nvm (Node Version Manager)
ENV NVM_DIR /usr/local/nvm
RUN mkdir -p $NVM_DIR
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.2/install.sh | bash

# Activate nvm
RUN . $NVM_DIR/nvm.sh

# Install specific version of Node with nvm and set it as default
RUN nvm install 16 && nvm alias default 16

# Set the working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY ./package.json .
RUN npm install

# Copy rest of the application
COPY . .
