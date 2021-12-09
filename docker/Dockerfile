FROM continuumio/miniconda3

WORKDIR /usr/src/app
COPY environment.yml .
RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "badger", "/bin/bash", "-c"]

# Demonstrate the environment is activated:
RUN echo "Make sure badger is installed:"
RUN python -c "import badger"

# The code to run when container is started:
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "badger", "badger"]
