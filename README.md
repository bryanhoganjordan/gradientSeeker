# gradientSeeker
Calculates the flattest area of land from an image.

Iteratively calculates gradients from an image in reducing search windows. The program is executed via ```gradientSeeker.py```.

There are four example images in the directory: ```deeWhy.png```, ```centennialPark.png```, ```collaroy.png```, ```powerStation.png```.

Output from the ```deeWhy.png``` example is:

```
OLD_CORDS:
{'leftTopCorner': [0, 0], 'leftBottomCorner': [0, 299], 'rightTopCorner': [596, 0], 'rightBottomCorner': [596, 299]}
QUAD: 3 NEW_CORDS:
{'leftTopCorner': [596, 299], 'leftBottomCorner': [596, 448], 'rightTopCorner': [894, 299], 'rightBottomCorner': [894, 448]}
********************
OLD_CORDS:
{'leftTopCorner': [596, 299], 'leftBottomCorner': [596, 448], 'rightTopCorner': [894, 299], 'rightBottomCorner': [894, 448]}
QUAD: 0 NEW_CORDS:
{'leftTopCorner': [596, 299], 'leftBottomCorner': [596, 373], 'rightTopCorner': [745, 299], 'rightBottomCorner': [745, 373]}
********************
OLD_CORDS:
{'leftTopCorner': [596, 299], 'leftBottomCorner': [596, 373], 'rightTopCorner': [745, 299], 'rightBottomCorner': [745, 373]}
QUAD: 2 NEW_CORDS:
{'leftTopCorner': [745, 299], 'leftBottomCorner': [745, 336], 'rightTopCorner': [819, 299], 'rightBottomCorner': [819, 336]}
********************
OLD_CORDS:
{'leftTopCorner': [745, 299], 'leftBottomCorner': [745, 336], 'rightTopCorner': [819, 299], 'rightBottomCorner': [819, 336]}
QUAD: 1 NEW_CORDS:
{'leftTopCorner': [745, 336], 'leftBottomCorner': [745, 354], 'rightTopCorner': [782, 336], 'rightBottomCorner': [782, 354]}
********************
OLD_CORDS:
{'leftTopCorner': [745, 336], 'leftBottomCorner': [745, 354], 'rightTopCorner': [782, 336], 'rightBottomCorner': [782, 354]}
QUAD: 2 NEW_CORDS:
{'leftTopCorner': [782, 336], 'leftBottomCorner': [782, 345], 'rightTopCorner': [800, 336], 'rightBottomCorner': [800, 345]}
********************
```

![alt text](https://github.com/bryanhoganjordan/gradientSeeker/deeWhyExampleOutput.png)
