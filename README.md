# Git tutorial

clone existing repository to htdocs:

    git clone https://github.com/jgkenney/tutorial.git

to push changes to github repository:

    git status
    git add *
    git commit -m "your commit message here"
    git push

to pull changes from repository:

    git pull

ALWAYS PULL BEFORE MAKING CHANGES

## Raspberry Pi 5 Temperature Reader

This repository now includes a comprehensive temperature monitoring tool for Raspberry Pi 5!

**Quick Start:**
```bash
python3 raspberry_pi_temp_reader.py
```

**Features:**
- Real-time CPU temperature monitoring
- Continuous monitoring mode
- Celsius and Fahrenheit support
- Automatic method detection (vcgencmd or thermal zone)
- Color-coded temperature status indicators

For detailed documentation, see [TEMPERATURE_READER_README.md](TEMPERATURE_READER_README.md)
