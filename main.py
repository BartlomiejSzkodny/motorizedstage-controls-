from programFiles.laserStageControll import LaserStageControll

def main() -> int:
    laserStageControll = LaserStageControll()
    laserStageControll.run()
    print("Program finished")
    return 0

if __name__ == "__main__":
    while True:
        main()
        if input("Do you want to run the program again? (y/n): ") == "n":
            break
