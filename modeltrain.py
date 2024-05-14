import numpy as np
from keras import Sequential
from sklearn.model_selection import train_test_split
from tensorflow import keras
from keras import layers
from keras.regularizers import l2
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Conv1D, MaxPooling1D, Flatten, Dense,Conv2D,MaxPooling2D,Dropout


# 构建半监督学习模型
def build_semisupervised_model(input_size):
    # 创建一个 Sequential 模型
    model = Sequential()

    # 添加第一个卷积层
    model.add(Conv2D(64, kernel_size=(3, 3), activation='relu', input_shape=(16, 15, 1)))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    # 添加第二个卷积层
    model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    # 添加扁平化层
    model.add(Flatten())

    # 添加全连接层
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))  # 添加 Dropout 层，减少过拟合

    # 添加输出层
    model.add(Dense(1, activation='linear'))

    # 编译模型
    model.compile(loss='mean_squared_error', optimizer='adam')


    return model

# 构建有标签数据的训练集
# labeled_data 是带有标签的数据集，包含输入数据和对应的目标标签
# 每个样本的标签可以是一个连续值
def build_labeled_dataset(wavpath):
    labeled_data = np.load(wavpath+'/'+'labeltraindate.npy')
    unlabel_date = np.load(wavpath+'/'+'unlabeltraindate.npy')
    label = np.load(wavpath+'/'+'trainlabeldate.npy')
    test_date = np.load(wavpath+'/'+'testmusicdate.npy')

    return labeled_data,unlabel_date,label,test_date

# 构建未标记数据的训练集
# unlabeled_data 是未标记的数据集，只包含输入数据，没有目标标签
def build_unlabeled_dataset(wavpath):
    unlabeled_dataset = np.load(wavpath+'/'+'trainunlabeldate.npy')

    return unlabeled_dataset


if __name__=="__main__":
    input_size = (16,15)
    # 构建半监督学习模型
    model = build_semisupervised_model(input_size)
    # 获取有标签数据集和未标记数据集
    labeled_date,unlabel_date,label,test_date = build_labeled_dataset(wavpath = "./trainset/classical/train")

    # 打乱数据
    np.random.seed(42)  # 设置随机种子以保持结果可重现
    shuffled_indices = np.random.permutation(len(labeled_date))
    x_train = labeled_date[shuffled_indices]
    y_train = label[shuffled_indices]
    
    for i in range(20):
        # 使用有标签数据进行有监督训练
        model.fit(x_train, y_train, batch_size=4, epochs=5)
        # 半监督学习
        unlabel_predictions = model.predict(unlabel_date)
        model.fit(unlabel_date, unlabel_predictions, batch_size=4, epochs=5)
        # 使用有标签数据进行有监督训练
        model.fit(x_train, y_train, batch_size=4, epochs=5)
        # 保存模型
        np.savetxt('./trainset/classical/train/predatefile/predate' + str(i + 1) + 'train.txt', model.predict(
            np.concatenate((labeled_date,unlabel_date))),fmt='%f')
        np.savetxt('./trainset/classical/train/predatefile/predate' + str(i + 1) + 'test.txt', model.predict(
            test_date), fmt='%f')
        model.save('./trainset/classical/train/model/my_model'+str(i+1)+'.h5')
    test=1


