import numpy as np
from stl import mesh

# 读取STL
blade = mesh.Mesh.from_file('Futher_Op_com4_SW.stl')

# 沿Y轴镜像（Y坐标取反）
blade.vectors[:, :, 1] *= -1  # 所有三角面片的所有顶点的Y坐标取反

# 镜像后需要翻转法线（交换每个三角形的两个顶点顺序）
for i in range(len(blade.vectors)):
    blade.vectors[i] = blade.vectors[i][[0, 2, 1]]  # 交换第2和第3个顶点

# 重新计算法线
blade.update_normals()

# 保存
blade.save('Futher_Op_com4_SW_mirrored.stl')

print("镜像完成！")
