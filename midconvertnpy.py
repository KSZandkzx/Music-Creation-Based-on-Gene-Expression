import numpy as np
import librosa
import mido
import subprocess

def extratmidi(midi_path, midi_savepath, wav_savepath):
    # 读取MIDI文件
    midi_file = mido.MidiFile(midi_path)
    # 选择一个特定的轨道（例如第一个轨道）

    # 创建一个新的MIDI文件对象
    merged_mid = mido.MidiFile()

    # 将合并的音轨添加到新的MIDI文件中
    merged_mid.tracks.append(midi_file.tracks[0])
    merged_mid.tracks.append(midi_file.tracks[1])

    # 保存合并后的MIDI文件
    merged_mid.save(midi_savepath)

    # 转化midi文件
    # 定义要运行的命令
    command = ['FluidSynth', '-F', wav_savepath, './sf2/YDPGrandPiano20160804.sf2',
               midi_savepath]
    # 运行命令并等待其完成
    with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
        output, error = process.communicate()
        if process.returncode != 0:
            print(f'An error occurred: {error}')

def get_offset(midi_path, audio_file):

    # 读取MIDI文件
    midi_file = mido.MidiFile(midi_path)
    # 选择一个特定的轨道（例如第一个轨道）
    track_index = 1
    track = midi_file.tracks[track_index]
    # 定义一个变量来记录当前时间
    current_time = 0
    # 遍历轨道的每个事件
    for event in track:
        if event.time != 0:
            # 更新当前时间
            if event.type == 'note_on' or event.type == 'note_off' or event.type == 'end_of_track':
                current_time += event.time

    audio_duration = librosa.get_duration(path=audio_file)

    if current_time==0:
        return 0
    else:
        return 1/current_time*audio_duration

def getnoteindex(midi_path, time, offset, sampletime):
    # 读取MIDI文件
    midi_file = mido.MidiFile(midi_path)
    # 选择一个特定的轨道（例如第一个轨道）
    track_index = 1
    track = midi_file.tracks[track_index]
    # 定义一个列表来存储音符的音高和时长
    noteindex = []
    # 定义一个变量来记录当前时间
    current_time = 0
    sumtime = 0
    # 遍历轨道的每个事件
    for event in track:
        if event.time != 0:
            if event.type == 'note_on' or event.type == 'note_off':
                # 如果事件类型是音符
                while (current_time + event.time) * offset > sumtime:
                    sumtime += sampletime
                    if event.velocity != 0:
                        noteindex.append(0)
                    else:
                        # 获取音符的音高和时长
                        note_pitch = event.note
                        noteindex.append(int(note_pitch))
            # 更新当前时间
            current_time += event.time

        if sumtime > time:
            break
    if sumtime > time:
        return noteindex
    else:
        return []

if __name__ == '__main__':

    # floderpath = './trainset/classical'
    # for i in range(443,849):
    #     extratmidi(floderpath+'/midfile/'+str(i)+'.mid',floderpath+'/extract/onechanel'+str(i)+'.mid',
    #                floderpath+'/extract/onechanel'+str(i)+'.wav')
    #     print(i)
    floderpath = './othermethod/0/'
    allnum = []
    time = 60
    sampletime = 0.25
    for i in range(177,200):
        offset = get_offset(floderpath+str(i)+'.mid',floderpath+str(i)+'.wav')
        if offset != 0:
            notenum = getnoteindex(floderpath+str(i)+'.mid',time,offset,sampletime)
            if len(notenum) != 0:
                notenum = np.array(notenum[0:int(time/sampletime)])
                notenumreshape = notenum.reshape(16,int(time/sampletime/16))
                allnum.append(notenumreshape)
                # print(len(notenum))
        print(i)
    print('availnum:',len(allnum))
    allnum_arry = np.array(allnum)
    np.save('./othermethod/compare/0.npy',allnum_arry)
    # np.save('./trainset/classical/train/badmusicdate.npy',allnum_arry)
    # test = 1