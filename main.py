from programFiles.laserStageControll import LaserStageControll
if __name__ == '__main__':
    try:
        # Create a new instance of the class
        LaserStageControll().run()
    except Exception as e:
        print(f"An error occurred: {e}")