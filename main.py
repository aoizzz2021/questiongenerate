import traceback
import sqlite3
import MainWindow
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
import sys
import qt_material
import random
import xlwt
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.font_manager import FontProperties

# windows下配置 font 为中文字体，自己去该路径找到自己电脑自带的字体
font = FontProperties(fname=r"C:\Windows\Fonts\Microsoft YaHei UI.ttc", size=14)

# 基本配置
knowledge_dic = {0: 'Python概述', 1: '运算及表达式', 2: '程序基础', 3: '序列', 4: '字典集合', 5: '函数', 6: '字符串', 7: '编程基础'}
type_dic = {0: '单选题', 1: '判断题', 2: '填空题', 3: '编程题', 4: '简答题', 5: '程序阅读'}
# 链接数据库
conn = sqlite3.connect('question.db')
cur = conn.cursor()

# 下面计算所有题型易、中、高的总数
sql = 'select count(1) from sourcedata where topic = "单选题"'
cur.execute(sql)
radio_sum = cur.fetchone()[0]
idx_sql = 'select idx from sourcedata where topic = "单选题" and dif = "易"'
cur.execute(idx_sql)
e_radio_lst = cur.fetchall()
idx_sql = 'select idx from sourcedata where topic = "单选题" and dif = "中"'
cur.execute(idx_sql)
m_radio_lst = cur.fetchall()
idx_sql = 'select idx from sourcedata where topic = "单选题" and dif = "高"'
cur.execute(idx_sql)
h_radio_lst = cur.fetchall()

sql = 'select count(1) from sourcedata where topic = "判断题"'
cur.execute(sql)
bool_sum = cur.fetchone()[0]
idx_sql = 'select idx from sourcedata where topic = "判断题" and dif = "易"'
cur.execute(idx_sql)
e_bool_lst = cur.fetchall()
idx_sql = 'select idx from sourcedata where topic = "判断题" and dif = "中"'
cur.execute(idx_sql)
m_bool_lst = cur.fetchall()
idx_sql = 'select idx from sourcedata where topic = "判断题" and dif = "高"'
cur.execute(idx_sql)
h_bool_lst = cur.fetchall()

sql = 'select count(1) from sourcedata where topic = "填空题"'
cur.execute(sql)
text_sum = cur.fetchone()[0]
idx_sql = 'select idx from sourcedata where topic = "填空题" and dif = "易"'
cur.execute(idx_sql)
e_text_lst = cur.fetchall()
idx_sql = 'select idx from sourcedata where topic = "填空题" and dif = "中"'
cur.execute(idx_sql)
m_text_lst = cur.fetchall()
idx_sql = 'select idx from sourcedata where topic = "填空题" and dif = "高"'
cur.execute(idx_sql)
h_text_lst = cur.fetchall()

sql = 'select count(1) from sourcedata where topic = "编程题"'
cur.execute(sql)
code_sum = cur.fetchone()[0]
idx_sql = 'select idx from sourcedata where topic = "编程题" and dif = "易"'
cur.execute(idx_sql)
e_code_lst = cur.fetchall()
idx_sql = 'select idx from sourcedata where topic = "编程题" and dif = "中"'
cur.execute(idx_sql)
m_code_lst = cur.fetchall()
idx_sql = 'select idx from sourcedata where topic = "编程题" and dif = "高"'
cur.execute(idx_sql)
h_code_lst = cur.fetchall()

sql = 'select count(1) from sourcedata where topic = "简答题"'
cur.execute(sql)
easyanswer_sum = cur.fetchone()[0]
idx_sql = 'select idx from sourcedata where topic = "简答题" and dif = "易"'
cur.execute(idx_sql)
e_easyanswer_lst = cur.fetchall()
idx_sql = 'select idx from sourcedata where topic = "简答题" and dif = "中"'
cur.execute(idx_sql)
m_easyanswer_lst = cur.fetchall()
idx_sql = 'select idx from sourcedata where topic = "简答题" and dif = "高"'
cur.execute(idx_sql)
h_easyanswer_lst = cur.fetchall()

sql = 'select count(1) from sourcedata where topic = "阅读程序"'
cur.execute(sql)
coderead_sum = cur.fetchone()[0]
idx_sql = 'select idx from sourcedata where topic = "阅读程序" and dif = "易"'
cur.execute(idx_sql)
e_coderead_lst = cur.fetchall()
idx_sql = 'select idx from sourcedata where topic = "阅读程序" and dif = "中"'
cur.execute(idx_sql)
m_coderead_lst = cur.fetchall()
idx_sql = 'select idx from sourcedata where topic = "阅读程序" and dif = "高"'
cur.execute(idx_sql)
h_coderead_lst = cur.fetchall()

sql = ''
idx_sql = ''


# ui的配置，设置画面按钮不可选
def set_knowledge_disabled(ui):
    ui.checkBox_1.setDisabled(True)
    ui.checkBox_2.setDisabled(True)
    ui.checkBox_3.setDisabled(True)
    ui.checkBox_4.setDisabled(True)
    ui.checkBox_5.setDisabled(True)
    ui.checkBox_6.setDisabled(True)
    ui.checkBox_7.setDisabled(True)
    ui.checkBox_8.setDisabled(True)

    ui.checkBox_haveknowledge.setChecked(False)


# 设置可选
def set_knowledge_enabled(ui):
    ui.checkBox_1.setDisabled(False)
    ui.checkBox_2.setDisabled(False)
    ui.checkBox_3.setDisabled(False)
    ui.checkBox_4.setDisabled(False)
    ui.checkBox_5.setDisabled(False)
    ui.checkBox_6.setDisabled(False)
    ui.checkBox_7.setDisabled(False)
    ui.checkBox_8.setDisabled(False)

    ui.checkBox_noknowledge.setChecked(False)


# 下面是设置按钮点中和取消，使得后面的输入框可选不可选
def set_radio_enabled(ui):
    if ui.lineEdit_radio.isEnabled():
        ui.lineEdit_radio.setDisabled(True)
        ui.lineEdit_radio_sum.setDisabled(True)
    else:
        ui.lineEdit_radio.setDisabled(False)
        ui.lineEdit_radio_sum.setDisabled(False)


# 同上
def set_bool_enabled(ui):
    if ui.lineEdit_bool.isEnabled():
        ui.lineEdit_bool.setDisabled(True)
        ui.lineEdit_bool_sum.setDisabled(True)
    else:
        ui.lineEdit_bool.setDisabled(False)
        ui.lineEdit_bool_sum.setDisabled(False)


# 同上
def set_code_enabled(ui):
    if ui.lineEdit_code.isEnabled():
        ui.lineEdit_code.setDisabled(True)
        ui.lineEdit_code_sum.setDisabled(True)
    else:
        ui.lineEdit_code.setDisabled(False)
        ui.lineEdit_code_sum.setDisabled(False)


# 同上
def set_coderead_enabled(ui):
    if ui.lineEdit_coderead.isEnabled():
        ui.lineEdit_coderead.setDisabled(True)
        ui.lineEdit_coderead_sum.setDisabled(True)
    else:
        ui.lineEdit_coderead.setDisabled(False)
        ui.lineEdit_coderead_sum.setDisabled(False)


# 同上
def set_easyanswer_enabled(ui):
    if ui.lineEdit_easyanswer.isEnabled():
        ui.lineEdit_easyanswer.setDisabled(True)
        ui.lineEdit_easyanswer_sum.setDisabled(True)
    else:
        ui.lineEdit_easyanswer.setDisabled(False)
        ui.lineEdit_easyanswer_sum.setDisabled(False)


# 同上
def set_text_enabled(ui):
    if ui.lineEdit_text.isEnabled():
        ui.lineEdit_text.setDisabled(True)
        ui.lineEdit_text_sum.setDisabled(True)
    else:
        ui.lineEdit_text.setDisabled(False)
        ui.lineEdit_text_sum.setDisabled(False)


# 获取excel内容存入数据库，只要第一次选择文件，后面就不用重新选了，如果更新了题库可以重选一次
def get_filepath():
    conn = sqlite3.connect('question.db')
    cur = conn.cursor()
    xls_path = QFileDialog.getOpenFileName()[0]
    try:
        sql = 'delete from sourcedata'
        cur.execute(sql)
        conn.commit()
        df = pd.read_excel(xls_path)
        for i in range(df.shape[0]):
            sql = 'INSERT INTO "sourcedata" ("idx","knowledge", "topic", "content", "answer", "parser", "dif", "goal", "count", "a", "b", "c", "d", "e", "f", "g") VALUES (' + str(
                i) + ','
            for item in df.iloc[i]:
                if type(item) == str:
                    item = item.replace("'", '"')
                sql += "'" + str(item) + "',"
            sql = sql[:-1] + ")"
            cur.execute(sql)
            conn.commit()
        print('insert success')

        # 这里往下是重新计算各题型所有难易度的总数，因为可能会更新题库，所以得再执行一次
        global radio_sum, e_radio_lst, m_radio_lst, h_radio_lst, bool_sum, e_bool_lst, m_bool_lst, h_bool_lst, text_sum, e_text_lst, m_text_lst, h_text_lst, code_sum, e_code_lst, m_code_lst, h_code_lst, easyanswer_sum, e_easyanswer_lst, m_easyanswer_lst, h_easyanswer_lst, coderead_sum, e_coderead_lst, m_coderead_lst, h_coderead_lst
        sql = 'select count(1) from sourcedata where topic = "单选题"'
        cur.execute(sql)
        radio_sum = cur.fetchone()[0]
        idx_sql = 'select idx from sourcedata where topic = "单选题" and dif = "易"'
        cur.execute(idx_sql)
        e_radio_lst = cur.fetchall()
        idx_sql = 'select idx from sourcedata where topic = "单选题" and dif = "中"'
        cur.execute(idx_sql)
        m_radio_lst = cur.fetchall()
        idx_sql = 'select idx from sourcedata where topic = "单选题" and dif = "高"'
        cur.execute(idx_sql)
        h_radio_lst = cur.fetchall()

        sql = 'select count(1) from sourcedata where topic = "判断题"'
        cur.execute(sql)
        bool_sum = cur.fetchone()[0]
        idx_sql = 'select idx from sourcedata where topic = "判断题" and dif = "易"'
        cur.execute(idx_sql)
        e_bool_lst = cur.fetchall()
        idx_sql = 'select idx from sourcedata where topic = "判断题" and dif = "中"'
        cur.execute(idx_sql)
        m_bool_lst = cur.fetchall()
        idx_sql = 'select idx from sourcedata where topic = "判断题" and dif = "高"'
        cur.execute(idx_sql)
        h_bool_lst = cur.fetchall()

        sql = 'select count(1) from sourcedata where topic = "填空题"'
        cur.execute(sql)
        text_sum = cur.fetchone()[0]
        idx_sql = 'select idx from sourcedata where topic = "填空题" and dif = "易"'
        cur.execute(idx_sql)
        e_text_lst = cur.fetchall()
        idx_sql = 'select idx from sourcedata where topic = "填空题" and dif = "中"'
        cur.execute(idx_sql)
        m_text_lst = cur.fetchall()
        idx_sql = 'select idx from sourcedata where topic = "填空题" and dif = "高"'
        cur.execute(idx_sql)
        h_text_lst = cur.fetchall()

        sql = 'select count(1) from sourcedata where topic = "编程题"'
        cur.execute(sql)
        code_sum = cur.fetchone()[0]
        idx_sql = 'select idx from sourcedata where topic = "编程题" and dif = "易"'
        cur.execute(idx_sql)
        e_code_lst = cur.fetchall()
        idx_sql = 'select idx from sourcedata where topic = "编程题" and dif = "中"'
        cur.execute(idx_sql)
        m_code_lst = cur.fetchall()
        idx_sql = 'select idx from sourcedata where topic = "编程题" and dif = "高"'
        cur.execute(idx_sql)
        h_code_lst = cur.fetchall()

        sql = 'select count(1) from sourcedata where topic = "简答题"'
        cur.execute(sql)
        easyanswer_sum = cur.fetchone()[0]
        idx_sql = 'select idx from sourcedata where topic = "简答题" and dif = "易"'
        cur.execute(idx_sql)
        e_easyanswer_lst = cur.fetchall()
        idx_sql = 'select idx from sourcedata where topic = "简答题" and dif = "中"'
        cur.execute(idx_sql)
        m_easyanswer_lst = cur.fetchall()
        idx_sql = 'select idx from sourcedata where topic = "简答题" and dif = "高"'
        cur.execute(idx_sql)
        h_easyanswer_lst = cur.fetchall()

        sql = 'select count(1) from sourcedata where topic = "阅读程序"'
        cur.execute(sql)
        coderead_sum = cur.fetchone()[0]
        idx_sql = 'select idx from sourcedata where topic = "阅读程序" and dif = "易"'
        cur.execute(idx_sql)
        e_coderead_lst = cur.fetchall()
        idx_sql = 'select idx from sourcedata where topic = "阅读程序" and dif = "中"'
        cur.execute(idx_sql)
        m_coderead_lst = cur.fetchall()
        idx_sql = 'select idx from sourcedata where topic = "阅读程序" and dif = "高"'
        cur.execute(idx_sql)
        h_coderead_lst = cur.fetchall()

    except:
        print(traceback.format_exc())


# 主要的生成逻辑
def generate_res(ui):
    # 编写程序 25分 简答题5分 程序阅读20分 其他1分

    radio_count = 0
    bool_count = 0
    text_count = 0
    code_count = 0
    easyanswer_count = 0
    coderead_count = 0

    # 看选择的难易度
    dif_flag = 0
    if ui.radioButton_easy.isChecked():
        dif_flag = 0
    elif ui.radioButton_mid.isChecked():
        dif_flag = 1
    elif ui.radioButton_hard.isChecked():
        dif_flag = 2

    # 看选择了哪些知识点
    knowledge_lst = []
    type_lst = []
    if not ui.checkBox_noknowledge.isChecked():
        if ui.checkBox_1.isChecked():
            knowledge_lst.append('Python概述')
        if ui.checkBox_2.isChecked():
            knowledge_lst.append('运算及表达式')
        if ui.checkBox_3.isChecked():
            knowledge_lst.append('程序基础')
        if ui.checkBox_4.isChecked():
            knowledge_lst.append('序列')
        if ui.checkBox_5.isChecked():
            knowledge_lst.append('字典集合')
        if ui.checkBox_6.isChecked():
            knowledge_lst.append('函数')
        if ui.checkBox_7.isChecked():
            knowledge_lst.append('字符串')
        if ui.checkBox_8.isChecked():
            knowledge_lst.append('编程基础')

    # 获取总分，获取各题型的分数和题量，并计算新的总分
    try:
        all_sum = int(ui.lineEdit_all_sum.text())
    except:
        all_sum = 0
    topic_sum = 0
    if ui.checkBox_radio.isChecked():
        type_lst.append([0, int(ui.lineEdit_radio.text())])
        try:
            radio_count = int(ui.lineEdit_radio_sum.text())
        except:
            pass
        topic_sum += int(ui.lineEdit_radio.text())
    if ui.checkBox_bool.isChecked():
        type_lst.append([1, int(ui.lineEdit_bool.text())])
        try:
            bool_count = int(ui.lineEdit_bool_sum.text())
        except:
            pass
        topic_sum += int(ui.lineEdit_bool.text())
    if ui.checkBox_text.isChecked():
        type_lst.append([2, int(ui.lineEdit_text.text())])
        try:
            text_count = int(ui.lineEdit_text_sum.text())
        except:
            pass
        topic_sum += int(ui.lineEdit_text.text())
    if ui.checkBox_code.isChecked():
        type_lst.append([3, int(ui.lineEdit_code.text())])
        try:
            code_count = int(ui.lineEdit_code_sum.text())
        except:
            pass
        topic_sum += int(ui.lineEdit_code.text())
    if ui.checkBox_easyanswer.isChecked():
        type_lst.append([4, int(ui.lineEdit_easyanswer.text())])
        try:
            easyanswer_count = int(ui.lineEdit_easyanswer_sum.text())
        except:
            pass
        topic_sum += int(ui.lineEdit_easyanswer.text())
    if ui.checkBox_coderead.isChecked():
        type_lst.append([5, int(ui.lineEdit_coderead.text())])
        try:
            coderead_count = int(ui.lineEdit_coderead_sum.text())
        except:
            pass
        topic_sum += int(ui.lineEdit_coderead.text())

    # 报警提示，总分不符合啊，题量为空什么的
    if all_sum == 0:
        QMessageBox.warning(window, '警告', '总分不可为0', QMessageBox.Close)
    elif all_sum != topic_sum:
        QMessageBox.warning(window, '警告', '实际分数与总分不一致，实际分数：' + str(topic_sum), QMessageBox.Close)
    else:
        msg = ''
        for item in type_lst:
            if item[1] == '':
                msg += type_dic[item[0]] + '分值不能为空\n'
        if (radio_count == 0 and ui.checkBox_radio.isChecked()) or (
                bool_count == 0 and ui.checkBox_bool.isChecked()) or (
                text_count == 0 and ui.checkBox_text.isChecked()) or (
                code_count == 0 and ui.checkBox_code.isChecked()) or (
                easyanswer_count == 0 and ui.checkBox_easyanswer.isChecked()) or (
                coderead_count == 0 and ui.checkBox_coderead.isChecked()):
            msg += '题量不能为空！\n'
        if msg != '':
            QMessageBox.warning(window, '警告', msg, QMessageBox.Close)

        # 获取题目的逻辑，执行两次，分AB卷
        try:
            get_topic(knowledge_lst, radio_count, bool_count, text_count, code_count, easyanswer_count, coderead_count,
                      dif_flag,
                      'A')
            get_topic(knowledge_lst, radio_count, bool_count, text_count, code_count, easyanswer_count, coderead_count,
                      dif_flag,
                      'B')
        except:
            print(traceback.format_exc())


# 获取题目
def get_topic(knowledge_lst, radio_count, bool_count, text_count, code_count, easyanswer_count, coderead_count,
              dif_flag,
              ques_flag):
    # 计算各题型占比
    type_src = {}
    type_count = radio_count + bool_count + text_count + code_count + easyanswer_count + coderead_count
    if radio_count != 0:
        type_src['单选题'] = 100 * radio_count / type_count
    if bool_count != 0:
        type_src['判断题'] = 100 * bool_count / type_count
    if text_count != 0:
        type_src['填空题'] = 100 * text_count / type_count
    if code_count != 0:
        type_src['编程题'] = 100 * code_count / type_count
    if easyanswer_count != 0:
        type_src['简答题'] = 100 * easyanswer_count / type_count
    if coderead_count != 0:
        type_src['程序阅读题'] = 100 * coderead_count / type_count
    conn = sqlite3.connect('question.db')
    cur = conn.cursor()
    # 在这里修改比例，因为没有难的题目，难的比例是0
    try:
        if dif_flag == 0:
            res_topic_idx_lst, knowledge_src_dic = generate_topic(knowledge_lst, radio_count, bool_count, text_count,
                                                                  code_count, easyanswer_count, coderead_count, 0.6,
                                                                  0.4, 0)
        elif dif_flag == 1:
            res_topic_idx_lst, knowledge_src_dic = generate_topic(knowledge_lst, radio_count, bool_count, text_count,
                                                                  code_count, easyanswer_count, coderead_count, 0.4,
                                                                  0.6, 0)
        # elif dif_flag == 2:
        #     res_topic_idx_lst,knowledge_src_dic = generate_topic(knowledge_lst,radio_count, bool_count, text_count, code_count, easyanswer_count, coderead_count, 0.4,
        #                              0.6, 0)
    except:
        print(traceback.format_exc())

    # 新建excel，写入所有的题目
    wb = xlwt.Workbook()
    sht = wb.add_sheet('question')
    row_count = 1
    sht.write(0, 0, '目录')
    sht.write(0, 1, '题型')
    sht.write(0, 2, '题干')
    sht.write(0, 3, '正确答案')
    sht.write(0, 4, '答案解析')
    sht.write(0, 5, '难易度')
    sht.write(0, 6, '建议分数')
    sht.write(0, 7, '选项数')
    sht.write(0, 8, 'A')
    sht.write(0, 9, 'B')
    sht.write(0, 10, 'C')
    sht.write(0, 11, 'D')
    sht.write(0, 12, 'E')
    sht.write(0, 13, 'F')
    sht.write(0, 14, 'G')

    for item in res_topic_idx_lst:
        sql = 'select * from sourcedata where idx = ' + str(item[0])
        cur.execute(sql)
        res = cur.fetchone()
        topic_type = res[2]
        for i in range(len(res) - 1):
            if i != 6:
                if res[i + 1] != 'nan':
                    sht.write(row_count, i, str(res[i + 1]))
                else:
                    sht.write(row_count, i, '')
            else:
                if topic_type == '单选题':
                    sht.write(row_count,i,str(int(int(ui.lineEdit_radio.text())/radio_count)))
                elif topic_type == '判断题':
                    sht.write(row_count, i, str(int(int(ui.lineEdit_bool.text()) / bool_count)))
                elif topic_type == '填空题':
                    sht.write(row_count, i, str(int(int(ui.lineEdit_text.text()) / text_count)))
                elif topic_type == '编程题':
                    sht.write(row_count, i, str(int(int(ui.lineEdit_code.text()) / code_count)))
                elif topic_type == '简答题':
                    sht.write(row_count, i, str(int(int(ui.lineEdit_easyanswer.text()) / easyanswer_count)))
                elif topic_type == '阅读程序':
                    sht.write(row_count, i, str(int(int(ui.lineEdit_coderead.text()) / coderead_count)))
        row_count += 1

    wb.save('question' + ques_flag + '.xls')

    # 绘制两张饼图
    names = type_src.keys()
    percents = type_src.values()
    patches, l_text, p_text = plt.pie(percents, labels=names, autopct="%.2f%%")
    for t in l_text:
        t.set_fontproperties(matplotlib.font_manager.FontProperties(fname="simhei.ttf"))
    plt.savefig('Question type analysis pie chart ' + ques_flag + '.png')
    plt.close()
    names = knowledge_src_dic.keys()
    percents = knowledge_src_dic.values()
    patches, l_text, p_text = plt.pie(percents, labels=names, autopct="%.2f%%")
    for t in l_text:
        t.set_fontproperties(matplotlib.font_manager.FontProperties(fname="simhei.ttf"))
    plt.savefig('Knowledge point analysis pie chart ' + ques_flag + '.png')
    plt.close()

# 最终的逻辑，根据难易度计算各种难度题目总量，然后随机取题目，如果知识点不符合要求，重新随机
def generate_topic(knowledge_lst, radio_count, bool_count, text_count, code_count, easyanswer_count, coderead_count,
                   e_per, m_per, h_per):
    knowledge_src = []
    conn = sqlite3.connect('question.db')
    cur = conn.cursor()
    res_topic_idx_lst = []

    # 同样的逻辑执行6次
    e_radio_count = int(radio_count * e_per)
    m_radio_count = radio_count - e_radio_count
    # m_radio_count = int(radio_count * m_per)
    # h_radio_count = int(radio_count - e_radio_count - m_radio_count)
    for i in range(e_radio_count):
        radio_idx = random.randint(0, len(e_radio_lst) - 1)
        sql = 'select knowledge from sourcedata where idx =' + str(e_radio_lst[radio_idx][0])
        cur.execute(sql)
        knowledge_res = cur.fetchone()[0]
        flag_count = 0
        while knowledge_res not in knowledge_lst and flag_count < 15:
            flag_count += 1
            radio_idx = random.randint(0, len(e_radio_lst) - 1)
            sql = 'select knowledge from sourcedata where idx =' + str(e_radio_lst[radio_idx][0])
            cur.execute(sql)
            knowledge_res = cur.fetchone()[0]
        knowledge_src.append(knowledge_res)
        res_topic_idx_lst.append(e_radio_lst[radio_idx])
    for i in range(m_radio_count):
        radio_idx = random.randint(0, len(m_radio_lst) - 1)
        sql = 'select knowledge from sourcedata where idx =' + str(m_radio_lst[radio_idx][0])
        cur.execute(sql)
        knowledge_res = cur.fetchone()[0]
        flag_count = 0
        while knowledge_res not in knowledge_lst and flag_count < 15:
            flag_count += 1
            radio_idx = random.randint(0, len(m_radio_lst) - 1)
            sql = 'select knowledge from sourcedata where idx =' + str(m_radio_lst[radio_idx][0])
            cur.execute(sql)
            knowledge_res = cur.fetchone()[0]
        knowledge_src.append(knowledge_res)
        res_topic_idx_lst.append(m_radio_lst[radio_idx])
    # for i in range(h_radio_count):
    #     radio_idx = random.randint(0, len(h_radio_lst) - 1)
    #     sql = 'select knowledge from sourcedata where idx ='+str(h_radio_lst[radio_idx][0])
    #     cur.execute(sql)
    #     knowledge_res = cur.fetchone()[0]
    #     flag_count = 0
    #     while knowledge_res not in knowledge_lst and flag_count < 15:
    #         flag_count += 1
    #         radio_idx = random.randint(0, len(h_radio_lst) - 1)
    #         sql = 'select knowledge from sourcedata where idx =' + str(h_radio_lst[radio_idx][0])
    #         cur.execute(sql)
    #         knowledge_res = cur.fetchone()[0]
    #     knowledge_src.append(knowledge_res)
    #     res_topic_idx_lst.append(h_radio_lst[radio_idx])

    e_bool_count = int(bool_count * e_per)
    m_bool_count = bool_count - e_bool_count
    # m_bool_count = int(bool_count * m_per)
    # h_bool_count = int(bool_count - e_bool_count - m_bool_count)
    for i in range(e_bool_count):
        bool_idx = random.randint(0, len(e_bool_lst) - 1)
        sql = 'select knowledge from sourcedata where idx =' + str(e_bool_lst[bool_idx][0])
        cur.execute(sql)
        knowledge_res = cur.fetchone()[0]
        flag_count = 0
        while knowledge_res not in knowledge_lst and flag_count < 15:
            flag_count += 1
            bool_idx = random.randint(0, len(e_bool_lst) - 1)
            sql = 'select knowledge from sourcedata where idx =' + str(e_bool_lst[bool_idx][0])
            cur.execute(sql)
            knowledge_res = cur.fetchone()[0]
        knowledge_src.append(knowledge_res)
        res_topic_idx_lst.append(e_bool_lst[bool_idx])
    for i in range(m_bool_count):
        bool_idx = random.randint(0, len(m_bool_lst) - 1)
        sql = 'select knowledge from sourcedata where idx =' + str(m_bool_lst[bool_idx][0])
        cur.execute(sql)
        knowledge_res = cur.fetchone()[0]
        flag_count = 0
        while knowledge_res not in knowledge_lst and flag_count < 15:
            flag_count += 1
            bool_idx = random.randint(0, len(m_bool_lst) - 1)
            sql = 'select knowledge from sourcedata where idx =' + str(m_bool_lst[bool_idx][0])
            cur.execute(sql)
            knowledge_res = cur.fetchone()[0]
        knowledge_src.append(knowledge_res)
        res_topic_idx_lst.append(m_bool_lst[bool_idx])
    # for i in range(h_bool_count):
    #     bool_idx = random.randint(0, len(h_bool_lst) - 1)
    #     sql = 'select knowledge from sourcedata where idx ='+str(h_bool_lst[bool_idx][0])
    #     cur.execute(sql)
    #     knowledge_res = cur.fetchone()[0]
    #     flag_count = 0
    #     while knowledge_res not in knowledge_lst and flag_count < 15:
    #         flag_count += 1
    #         bool_idx = random.randint(0, len(h_bool_lst) - 1)
    #         sql = 'select knowledge from sourcedata where idx =' + str(h_bool_lst[bool_idx][0])
    #         cur.execute(sql)
    #         knowledge_res = cur.fetchone()[0]
    #     knowledge_src.append(knowledge_res)
    #     res_topic_idx_lst.append(h_bool_lst[bool_idx])

    e_text_count = int(text_count * e_per)
    m_text_count = text_count - e_text_count
    # m_text_count = int(text_count * m_per)
    # h_text_count = int(text_count - e_text_count - m_text_count)
    for i in range(e_text_count):
        text_idx = random.randint(0, len(e_text_lst) - 1)
        sql = 'select knowledge from sourcedata where idx =' + str(e_text_lst[text_idx][0])
        cur.execute(sql)
        knowledge_res = cur.fetchone()[0]
        flag_count = 0
        while knowledge_res not in knowledge_lst and flag_count < 15:
            flag_count += 1
            text_idx = random.randint(0, len(e_text_lst) - 1)
            sql = 'select knowledge from sourcedata where idx =' + str(e_text_lst[text_idx][0])
            cur.execute(sql)
            knowledge_res = cur.fetchone()[0]
        knowledge_src.append(knowledge_res)
        res_topic_idx_lst.append(e_text_lst[text_idx])
    for i in range(m_text_count):
        text_idx = random.randint(0, len(m_text_lst) - 1)
        sql = 'select knowledge from sourcedata where idx =' + str(m_text_lst[text_idx][0])
        cur.execute(sql)
        knowledge_res = cur.fetchone()[0]
        flag_count = 0
        while knowledge_res not in knowledge_lst and flag_count < 15:
            flag_count += 1
            text_idx = random.randint(0, len(m_text_lst) - 1)
            sql = 'select knowledge from sourcedata where idx =' + str(m_text_lst[text_idx][0])
            cur.execute(sql)
            knowledge_res = cur.fetchone()[0]
        knowledge_src.append(knowledge_res)
        res_topic_idx_lst.append(m_text_lst[text_idx])
    # for i in range(h_text_count):
    #     text_idx = random.randint(0, len(h_text_lst) - 1)
    #     sql = 'select knowledge from sourcedata where idx ='+str(h_text_lst[text_idx][0])
    #     cur.execute(sql)
    #     knowledge_res = cur.fetchone()[0]
    #     flag_count = 0
    #     while knowledge_res not in knowledge_lst and flag_count < 15:
    #         flag_count += 1
    #         text_idx = random.randint(0, len(h_text_lst) - 1)
    #         sql = 'select knowledge from sourcedata where idx =' + str(h_text_lst[text_idx][0])
    #         cur.execute(sql)
    #         knowledge_res = cur.fetchone()[0]
    #     knowledge_src.append(knowledge_res)
    #     res_topic_idx_lst.append(h_text_lst[text_idx])

    e_code_count = int(code_count * e_per)
    m_code_count = code_count - e_code_count
    # m_code_count = int(code_count * m_per)
    # h_code_count = int(code_count - e_code_count - m_code_count)
    for i in range(e_code_count):
        code_idx = random.randint(0, len(e_code_lst) - 1)
        sql = 'select knowledge from sourcedata where idx =' + str(e_code_lst[code_idx][0])
        cur.execute(sql)
        knowledge_res = cur.fetchone()[0]
        flag_count = 0
        while knowledge_res not in knowledge_lst and flag_count < 15:
            flag_count += 1
            code_idx = random.randint(0, len(e_code_lst) - 1)
            sql = 'select knowledge from sourcedata where idx =' + str(e_code_lst[code_idx][0])
            cur.execute(sql)
            knowledge_res = cur.fetchone()[0]
        knowledge_src.append(knowledge_res)
        res_topic_idx_lst.append(e_code_lst[code_idx])
    for i in range(m_code_count):
        code_idx = random.randint(0, len(m_code_lst) - 1)
        sql = 'select knowledge from sourcedata where idx =' + str(m_code_lst[code_idx][0])
        cur.execute(sql)
        knowledge_res = cur.fetchone()[0]
        flag_count = 0
        while knowledge_res not in knowledge_lst and flag_count < 15:
            flag_count += 1
            code_idx = random.randint(0, len(m_code_lst) - 1)
            sql = 'select knowledge from sourcedata where idx =' + str(m_code_lst[code_idx][0])
            cur.execute(sql)
            knowledge_res = cur.fetchone()[0]
        knowledge_src.append(knowledge_res)
        res_topic_idx_lst.append(m_code_lst[code_idx])
    # for i in range(h_code_count):
    #     code_idx = random.randint(0, len(h_code_lst) - 1)
    #     sql = 'select knowledge from sourcedata where idx ='+str(h_code_lst[code_idx][0])
    #     cur.execute(sql)
    #     knowledge_res = cur.fetchone()[0]
    #     flag_count = 0
    #     while knowledge_res not in knowledge_lst and flag_count < 15:
    #         flag_count += 1
    #         code_idx = random.randint(0, len(h_code_lst) - 1)
    #         sql = 'select knowledge from sourcedata where idx =' + str(h_code_lst[code_idx][0])
    #         cur.execute(sql)
    #         knowledge_res = cur.fetchone()[0]
    #     knowledge_src.append(knowledge_res)
    #     res_topic_idx_lst.append(h_code_lst[code_idx])

    e_easyanswer_count = int(easyanswer_count * e_per)
    m_easyanswer_count = easyanswer_count - e_easyanswer_count
    # m_easyanswer_count = int(easyanswer_count * m_per)
    # h_easyanswer_count = int(easyanswer_count - e_easyanswer_count - m_easyanswer_count)
    for i in range(e_easyanswer_count):
        easyanswer_idx = random.randint(0, len(e_easyanswer_lst) - 1)
        sql = 'select knowledge from sourcedata where idx =' + str(e_easyanswer_lst[easyanswer_idx][0])
        cur.execute(sql)
        knowledge_res = cur.fetchone()[0]
        flag_count = 0
        while knowledge_res not in knowledge_lst and flag_count < 15:
            flag_count += 1
            easyanswer_idx = random.randint(0, len(e_easyanswer_lst) - 1)
            sql = 'select knowledge from sourcedata where idx =' + str(e_easyanswer_lst[easyanswer_idx][0])
            cur.execute(sql)
            knowledge_res = cur.fetchone()[0]
        knowledge_src.append(knowledge_res)
        res_topic_idx_lst.append(e_easyanswer_lst[easyanswer_idx])
    for i in range(m_easyanswer_count):
        easyanswer_idx = random.randint(0, len(m_easyanswer_lst) - 1)
        sql = 'select knowledge from sourcedata where idx =' + str(m_easyanswer_lst[easyanswer_idx][0])
        cur.execute(sql)
        knowledge_res = cur.fetchone()[0]
        flag_count = 0
        while knowledge_res not in knowledge_lst and flag_count < 15:
            flag_count += 1
            easyanswer_idx = random.randint(0, len(m_easyanswer_lst) - 1)
            sql = 'select knowledge from sourcedata where idx =' + str(m_easyanswer_lst[easyanswer_idx][0])
            cur.execute(sql)
            knowledge_res = cur.fetchone()[0]
        knowledge_src.append(knowledge_res)
        res_topic_idx_lst.append(m_easyanswer_lst[easyanswer_idx])
    # for i in range(h_easyanswer_count):
    #     easyanswer_idx = random.randint(0, len(h_easyanswer_lst) - 1)
    #     sql = 'select knowledge from sourcedata where idx ='+str(h_easyanswer_lst[easyanswer_idx][0])
    #     cur.execute(sql)
    #     knowledge_res = cur.fetchone()[0]
    #     flag_count = 0
    #     while knowledge_res not in knowledge_lst and flag_count < 15:
    #         flag_count += 1
    #         easyanswer_idx = random.randint(0, len(h_easyanswer_lst) - 1)
    #         sql = 'select knowledge from sourcedata where idx =' + str(h_easyanswer_lst[easyanswer_idx][0])
    #         cur.execute(sql)
    #         knowledge_res = cur.fetchone()[0]
    #     knowledge_src.append(knowledge_res)
    #     res_topic_idx_lst.append(h_easyanswer_lst[easyanswer_idx])

    e_coderead_count = int(coderead_count * e_per)
    m_coderead_count = coderead_count - e_coderead_count
    # m_coderead_count = int(coderead_count * 0.2)
    # h_coderead_count = int(coderead_count - e_coderead_count - m_coderead_count)
    for i in range(e_coderead_count):
        coderead_idx = random.randint(0, len(e_coderead_lst) - 1)
        sql = 'select knowledge from sourcedata where idx =' + str(e_coderead_lst[coderead_idx][0])
        cur.execute(sql)
        knowledge_res = cur.fetchone()[0]
        flag_count = 0
        while knowledge_res not in knowledge_lst and flag_count < 15:
            flag_count += 1
            coderead_idx = random.randint(0, len(e_coderead_lst) - 1)
            sql = 'select knowledge from sourcedata where idx =' + str(e_coderead_lst[coderead_idx][0])
            cur.execute(sql)
            knowledge_res = cur.fetchone()[0]
        knowledge_src.append(knowledge_res)
        res_topic_idx_lst.append(e_coderead_lst[coderead_idx])
    for i in range(m_coderead_count):
        coderead_idx = random.randint(0, len(m_coderead_lst) - 1)
        sql = 'select knowledge from sourcedata where idx =' + str(m_coderead_lst[coderead_idx][0])
        cur.execute(sql)
        knowledge_res = cur.fetchone()[0]
        flag_count = 0
        while knowledge_res not in knowledge_lst and flag_count < 15:
            flag_count += 1
            coderead_idx = random.randint(0, len(m_coderead_lst) - 1)
            sql = 'select knowledge from sourcedata where idx =' + str(m_coderead_lst[coderead_idx][0])
            cur.execute(sql)
            knowledge_res = cur.fetchone()[0]
        knowledge_src.append(knowledge_res)
        res_topic_idx_lst.append(m_coderead_lst[coderead_idx])
    # for i in range(h_coderead_count):
    #     coderead_idx = random.randint(0, len(h_coderead_lst) - 1)
    #     sql = 'select knowledge from sourcedata where idx ='+str(h_coderead_lst[coderead_idx][0])
    #     cur.execute(sql)
    #     knowledge_res = cur.fetchone()[0]
    #     flag_count = 0
    #     while knowledge_res not in knowledge_lst and flag_count < 15:
    #         flag_count += 1
    #         coderead_idx = random.randint(0, len(h_coderead_lst) - 1)
    #         sql = 'select knowledge from sourcedata where idx =' + str(h_coderead_lst[coderead_idx][0])
    #         cur.execute(sql)
    #         knowledge_res = cur.fetchone()[0]
    #     knowledge_src.append(knowledge_res)
    #     res_topic_idx_lst.append(h_coderead_lst[coderead_idx])

    knowledge_src_dic = {}
    for item in knowledge_src:
        if knowledge_src_dic.get(item):
            knowledge_src_dic[item] += 1
        else:
            knowledge_src_dic[item] = 1
    for key in knowledge_src_dic.keys():
        knowledge_src_dic[key] = knowledge_src_dic[key] / len(knowledge_src)
    return res_topic_idx_lst, knowledge_src_dic

# 初始化页面，给每个按钮绑定下对应的方法
def init_ui(ui):
    ui.pushButton_selectpath.clicked.connect(lambda: get_filepath())
    ui.pushButton_generateres.clicked.connect(lambda: generate_res(ui))

    ui.radioButton_easy.setChecked(True)

    ui.checkBox_haveknowledge.setChecked(True)
    ui.checkBox_haveknowledge.clicked.connect(lambda: set_knowledge_enabled(ui))
    ui.checkBox_noknowledge.clicked.connect(lambda: set_knowledge_disabled(ui))

    ui.checkBox_radio.clicked.connect(lambda: set_radio_enabled(ui))
    ui.checkBox_bool.clicked.connect(lambda: set_bool_enabled(ui))
    ui.checkBox_code.clicked.connect(lambda: set_code_enabled(ui))
    ui.checkBox_coderead.clicked.connect(lambda: set_coderead_enabled(ui))
    ui.checkBox_easyanswer.clicked.connect(lambda: set_easyanswer_enabled(ui))
    ui.checkBox_text.clicked.connect(lambda: set_text_enabled(ui))

# 入口函数
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # 判断下表有没有建，没有的话新建下
    conn = sqlite3.connect('question.db')
    cur = conn.cursor()
    sql = """CREATE TABLE if not exists  "sourcedata" (
            "idx" INTEGER NULL DEFAULT NULL,
	        "knowledge" VARCHAR(50) NULL DEFAULT NULL,
	        "topic" VARCHAR(50) NULL DEFAULT NULL,
	        "content" VARCHAR(50) NULL DEFAULT NULL,
	        "answer" VARCHAR(50) NULL DEFAULT NULL,
	        "parser" VARCHAR(50) NULL DEFAULT NULL,
	        "dif" VARCHAR(50) NULL DEFAULT NULL,
	        "goal" INTEGER NULL DEFAULT NULL,
	        "count" INTEGER NULL DEFAULT NULL,
	        "a" VARCHAR(50) NULL DEFAULT NULL,
	        "b" VARCHAR(50) NULL DEFAULT NULL,
	        "c" VARCHAR(50) NULL DEFAULT NULL,
	        "d" VARCHAR(50) NULL DEFAULT NULL,
	        "e" VARCHAR(50) NULL DEFAULT NULL,
	        "f" VARCHAR(50) NULL DEFAULT NULL,
	        "g" VARCHAR(50) NULL DEFAULT NULL
                )
                ;"""
    cur.execute(sql)
    conn.commit()

    window = QMainWindow()
    ui = MainWindow.Ui_MainWindow()
    ui.setupUi(window)
    # 这里可以改页面风格，theme='dark_cyan.xml'，修改xml文件名即可
    app.setStyle(qt_material.apply_stylesheet(app, theme='dark_cyan.xml'))
    init_ui(ui)
    window.show()

    sys.exit(app.exec_())
