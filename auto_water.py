import water

if __name__ == "__main__":
    f = open("tankCapacity.txt", "r")
    value = f.read()
    float(value)
    water.auto_water(float(value))
    f.close()
