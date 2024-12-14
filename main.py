from programFiles.laserStageControll import LaserStageControll

def main() -> int:
    laserStageControll = LaserStageControll()
    laserStageControll.run()
    return 0

if __name__ == "__main__":
    while True:
        main()
        if input("Do you want to close the program?(y/n): ") == "y":
            break
