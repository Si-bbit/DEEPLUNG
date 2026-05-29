# -*- mode: python ; coding: utf-8 -*-
 
a = Analysis(
    ['predictUI_copy_3.py'],
    pathex=['.'],  # 修改1：添加当前目录，确保能找到自定义模块 
    binaries=[],
    datas=[
        # 修改2：路径分隔符改为 / 或使用 raw string，避免转义错误 
        ('modelpth/UBUNep500-loss0.310-val_loss0.414.pth', 'weights'),
        ('modelpth/ep300-loss0.013-val_loss0.043.pth', 'weights'),
        # 修改3：添加UI用到的静态资源（必须与代码中修改后的相对路径对应）
        ('images/UI/logo.jpg', 'images/UI'),
        ('images/UI/zhu.jpg', 'images/UI'),
        ('style/hospital_theme.qss', 'style'),
        ('unet.py', '.'),
        ('deeplab.py', '.'),
        ('nets', 'nets'),   # 把整个 nets 文件夹打包进去 
        ('utils', 'utils'), # 把整个 utils 文件夹打包进去 
    
       # ('D:/DL/unet-pytorch4ear/FINALGUI/dist/xinghuoUIs2/xinghuoUIs2.exe', '.'),
       # ('D:/DL/unet-pytorch4ear/FINALGUI/dist/xinghuoUIs/xinghuoUIs.exe', '.')

    ],
    hiddenimports=[
        # --- 原有的 ---
        'torch', 'torchvision', 'torch.nn', 'torch.utils.data',
        'cv2', 'numpy', 'yaml',
        
        # --- 修改4：必须添加你项目自定义的模块！！！ ---
        'deeplab', 'unet',
        'nets', 'nets.deeplabv3_plus', 'nets.unet',
        'utils', 'utils.utils',
        
        # --- 修改5：添加 PySide6 和 其他缺失的库 ---
        'PySide6.QtWidgets', 'PySide6.QtGui', 'PySide6.QtCore',
        'pydicom',
        
        # --- 修改6：如果 backbone 用了 resnet/mobilenet，必须加下面这行 ---
        'torchvision.models.resnet', 'torchvision.models.mobilenet', 
        'torchvision.models._api',
        'pydicom',
        'pydicom.encoders',
        'pydicom.encoders.gdcm',    # 解决你当前的报错 
        'pydicom.encoders.pylibjpeg', # 防患于未然 
        'pydicom.encoders.native',    # 防患于未然 
        'gdcm',                       # gdcm 核心模块 
        'pylibjpeg',                  # pylibjpeg 核心模块 
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # 修改7：删除 'matplotlib'！！！你的代码里用到了 matplotlib 画图，排除了会直接报错崩溃 
        'ultralytics', 'jupyter', 'tkinter', 'IPython'
    ],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)
 
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='深肺智影',  # 可以把名字改得好看点 
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # 调试阶段建议保持 True，方便看报错。确认无误后改为 False 
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='深肺智影',
)