sqrt_companding_table = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,25,27,29,31,33,35,37,39,41,43,45,47,49,51,53,55,57,59,61,63,67,71,75,79,83,87,91,95,99,103,107,111,115,119,123,127,131,135,139,143,147,151,155,159,163,167,171,175,179,183,187,191,195,199,203,207,211,215,219,223,227,231,235,239,243,247,255,263,271,279,287,295,303,311,319,327,335,343,351,359,367,375,383,391,399,407,415,423,431,439,447,455,463,471,479,487,495,503,511,519,527,535,543,551,559,567,575,583,591,599,607,615,623,631,639,647,655,663,671,679,687,695,703,711,719,727,735,743,751,759,767,775,783,791,799,807,815,823,831,839,847,855,863,871,879,887,895,903,911,919,927,935,943,951,959,967,975,983,991,999,1007,1023,1039,1055,1071,1087,1103,1119,1135,1151,1167,1183,1199,1215,1231,1247,1263,1279,1295,1311,1327,1343,1359,1375,1391,1407,1439,1471,1503,1535,1567,1599,1631,1663,1695,1727,1759,1791,1823,1855,1887,1919,1951,1983,2015,2047,2079,2111,2143,2175,2207,2239,2271,2303,2335,2367,2399,2431,2463,2495,2527,2559,2591,2623,2655,2687,2719,2751,2783,2815,2847,2879]
def clamp(n, smallest, largest): return max(smallest, min(n, largest))

def bugged_pixel(image, x, y, width, height):
    val = 0.0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if 0 <= x + i < width:
                if 0 <= y + j < height:
                    if i == 0 and j == 0:
                        val += 3*image.getpixel((x + i,y + j))
                    else:
                        val -= image.getpixel((x + i, y + j))
    val /= 9
    return val

def avg_pixel(image, x, y, width, height):
    val = 0.0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if 0 <= x + i < width:
                if 0 <= y + j < height:
                    if i != 0 and j != 0:
                        val += image.getpixel((x + i,y + j))
    val /= 8
    return val