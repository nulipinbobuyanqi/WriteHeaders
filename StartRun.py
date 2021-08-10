# coding:utf-8
# @Author: wang_cong
# @File: StartRun.py
# @Project: AutoCreateCaseTool
# @Time: 2021/5/31 19:12


import os
import re
import time
from Utils.copy_files import copy_all_files
from Utils.create_case_yml_file import create_case_yml_file
from Utils.create_test_data import create_test_data
from Utils.get_changed_interface_info import get_summary_changed_interface_info, \
    get_method_changed_interface_info, get_parameter_type_changed_interface_info, get_parameter_changed_interface_info, \
    get_header_changed_interface_info
from Utils.get_delete_interface_info import get_deleted_interface_info
from Utils.get_deprecated_interface_info import get_all_deprecated_interfaces
from Utils.get_new_interface_info import get_new_interface_info
from Utils.get_no_change_interface_info import get_no_changes_interface_info
from Utils.get_project_config import get_project_config_info
from Utils.operation_dir import create_every_path_dirs
from Utils.operation_json import get_json_data
from Utils.operation_yml import get_yaml_data, save_ruamel_data

# 第八步：获取当前日期，作为接口版本号
new = time.strftime("%Y-%m-%d", time.localtime())
# new = "2021-08-05"

# 第一步：获取项目配置信息的存放根路径
project_yaml_path = "."
project_yaml_file_name = "project_path"
gen_path = get_yaml_data(project_yaml_path, project_yaml_file_name)["project_path"]
project_path = gen_path + "/ProjectManage/"
project_config_path = project_path + "01.ProjectConfig"
if not os.path.exists(project_config_path):
    os.makedirs(project_config_path)
# 第二步：获取项目配置信息
project, protocol, swagger_url = get_project_config_info(project_path)
# 第三步：创建接口信息json文件的存放根目录
interfaces_gen_path = project_path + "02.InterfaceData" + "/" + project
if not os.path.exists(interfaces_gen_path):
    os.makedirs(interfaces_gen_path)
#
new_interface_path = interfaces_gen_path + "/" + new
if not os.path.exists(new_interface_path):
    os.makedirs(new_interface_path)
# 第四步：创建接口信息模板yml文件存放根目录
api_template_gen_path = project_path + "03.InterfaceTemplate" + "/" + project
if not os.path.exists(api_template_gen_path):
    os.makedirs(api_template_gen_path)
#
new_api_path = api_template_gen_path + "/" + new
if not os.path.exists(new_api_path):
    os.makedirs(new_api_path)
# 第五步：创建测试用例模板yml文件存放根目录
case_template_gen_path = project_path + "05.CaseTemplate" + "/" + project
if not os.path.exists(case_template_gen_path):
    os.makedirs(case_template_gen_path)
#
new_case_path = case_template_gen_path + "/" + new
if not os.path.exists(new_case_path):
    os.mkdir(new_case_path)
# 第七步：创建所有的用例数据yml文件的存放根目录
all_cases_gen_path = project_path + "06.UnitTest/01.UnitCases" + "/" + project
if not os.path.exists(all_cases_gen_path):
    os.makedirs(all_cases_gen_path)
#
cases_path = all_cases_gen_path + "/" + new
if not os.path.exists(cases_path):
    os.mkdir(cases_path)
# 创建单元测试用例的脚本文件存放根目录
script_gen_path = project_path + "06.UnitTest/02.UnitCasesScripts" + "/" + project
if not os.path.exists(script_gen_path):
    os.makedirs(script_gen_path)
# 当前版本的单元测试的脚本文件目录
script_path = script_gen_path + "/" + new
if not os.path.exists(script_path):
    os.mkdir(script_path)
# 创建单元测试用例的运行配置文件存放根目录
run_config_gen_path = project_path + "06.UnitTest/03.UnitTestRunConfig" + "/" + project
if not os.path.exists(run_config_gen_path):
    os.makedirs(run_config_gen_path)
# 当前版本的单元测试的运行配置文件目录
run_config_path = run_config_gen_path + "/" + new
if not os.path.exists(run_config_path):
    os.mkdir(run_config_path)
# 创建单元测试用例的测试数据，如：各种文件，存放根目录
data_gen_path = project_path + "06.UnitTest/04.UnitTestData" + "/" + project
if not os.path.exists(data_gen_path):
    os.makedirs(data_gen_path)
# 当前版本的单元测试的测试数据，如：各种文件，目录
data_path = data_gen_path + "/" + new
if not os.path.exists(data_path):
    os.mkdir(data_path)
# 创建单元测试用例的报告存放根目录
report_gen_path = project_path + "06.UnitTest/05.UnitTestReport" + "/" + project
if not os.path.exists(report_gen_path):
    os.makedirs(report_gen_path)
# 当前版本的单元测试报告目录
report_path = report_gen_path + "/" + new
if not os.path.exists(report_path):
    os.mkdir(report_path)
# 创建单元测试用例的日志存放根目录
log_gen_path = project_path + "06.UnitTest/06.UnitTestLog" + "/" + project
if not os.path.exists(log_gen_path):
    os.makedirs(log_gen_path)
# 当前版本的单元测试日志目录
log_path = log_gen_path + "/" + new
if not os.path.exists(log_path):
    os.mkdir(log_path)
# 创建xml_report_path目录
xml_report_path = report_path + "/xml"
if not os.path.exists(xml_report_path):
    os.makedirs(xml_report_path)
# 创建detail_report_path目录
detail_report_path = report_path + "/detail_report"
if not os.path.exists(detail_report_path):
    os.makedirs(detail_report_path)
# 创建summary_report_path目录
summary_report_path = report_path + "/summary_report_path/summary_report.html"
# 创建测试报告的运行环境配置目录
environment_properties_path = xml_report_path
if not os.path.exists(environment_properties_path):
    os.makedirs(environment_properties_path)
# 创建单元测试用例的环境配置文件存放根目录
env_config_gen_path = project_path + "06.UnitTest/07.UnitTestEnvConfig" + "/" + project
if not os.path.exists(env_config_gen_path):
    os.makedirs(env_config_gen_path)
# 当前版本的单元测试的数据库环境配置文件目录
db_env_path = env_config_gen_path + "/" + new
if not os.path.exists(db_env_path):
    os.mkdir(db_env_path)
# 当前版本的单元测试的服务环境配置文件目录
service_env_path = env_config_gen_path + "/" + new
if not os.path.exists(service_env_path):
    os.mkdir(service_env_path)
# 创建单元测试用例的依赖配置文件存放根目录
depent_gen_path = project_path + "06.UnitTest/08.UnitTestDepentData" + "/" + project
if not os.path.exists(depent_gen_path):
    os.makedirs(depent_gen_path)
# 当前版本的单元测试的依赖配置文件目录
depent_path = depent_gen_path + "/" + new
if not os.path.exists(depent_path):
    os.mkdir(depent_path)
# 第十二步：无论是否首次测试该项目的接口，每个接口的yml文件的存放目录和case的yml文件存放目录，都需要创建好
new_json_data = get_json_data(new_interface_path, project)

# 获取请求头文件内容
request_headers = get_json_data(".", "request_headers")

# 获取所有已废弃的接口列表
all_deprecated_list = get_all_deprecated_interfaces(new_json_data)
# 没过滤掉废弃接口前的所有接口信息
new_paths = new_json_data["paths"]
"""
已被废弃的接口，即使接口的其他信息有所变化，也不去遍历，直接过滤掉
想要获取部分变更的接口，前提是：
1. 接口地址没有变化
2. 接口没有被废弃
"""
# 去除已废弃接口的所有接口信息
for depre in all_deprecated_list:
    new_paths.pop(depre)
new_path_list = list(new_paths.keys())
new_definition_list = []
all_new_definitions = new_json_data['definitions']
for definition in all_new_definitions:
    new_definition_list.append(definition)
for new_path in new_path_list:
    new_path = re.sub(r"{.*}", "", new_path, count=0, flags=0)
    create_every_path_dirs(new_api_path, new_path)
    create_every_path_dirs(new_case_path, new_path)
    create_every_path_dirs(cases_path, new_path)
    # 新增每个接口的测试数据的存放目录
    create_every_path_dirs(data_path, new_path)

all_case_file_list = create_case_yml_file(new_paths, new_case_path, new_definition_list, all_new_definitions, request_headers)
for every_case_file in all_case_file_list:
    if every_case_file.split("/")[-1] != "":
        file_name = every_case_file.split("/")[-1] + "_1"
    else:
        file_name = every_case_file.split("/")[-2] + "_1"
    data = get_yaml_data(every_case_file, file_name)
    data["case_common_info"]['interface_protocol'] = protocol
    save_ruamel_data(every_case_file, file_name, data)

# 第十四步：准备进行对比，拿json文件进行对比，得到版本的差异
if os.listdir(interfaces_gen_path)[0] == new:
    # print("首次进行该项目的接口测试，直接以当前日期为版本号，依次执行创建json文件、创建接口yml文件、创建用例yml文件")
    # print("无需进行比较")
    # 第十六步：复制现有的所有接口的yml文件到用例目录下，注意：若已有用例信息，需要仅变更用例信息的部分数据，而不是全部都被替换
    # 复制case前的原目录和复制case后的目录
    source_path = new_case_path
    target_path = cases_path
    copy_all_files(source_path, target_path, new)
else:
    # print("非首次测试该项目的接口")
    # print("需要进行比较")
    # 第十五步：在interfacedata目录下，列举出所有的版本日期，组成一个list，然后寻找到上个版本号日期，即:用来和当前日期版本进行比较
    all_version_list = list(os.listdir(interfaces_gen_path))
    # 最新版本日期为列表的最后一个值
    # 上个版本日期为列表的倒数第二个值
    old_version = all_version_list[-2]
    new_version = all_version_list[-1]
    new_interface_path = interfaces_gen_path + "/" + old_version
    old_json_data = get_json_data(new_interface_path, project)
    # 获取所有已废弃的接口列表
    all_old_deprecated_list = get_all_deprecated_interfaces(old_json_data)
    # 没过滤掉废弃接口前的所有接口信息
    old_paths = old_json_data["paths"]
    # 去除已废弃接口的所有接口信息
    for depre in all_old_deprecated_list:
        old_paths.pop(depre)
    # 将新增的接口，写入json文件中
    new_list, new_interface_info = get_new_interface_info(old_json_data, new_json_data)
    for every_interface in new_interface_info:
        every_interface["interface_protocol"] = protocol
    # 将删除的接口，写入json文件中
    delete_list = get_deleted_interface_info(old_json_data, new_json_data)
    # delete的接口，本就不会被创建目录和生成接口yml文件、用例yml文件，所以，无需处理删除
    # 将变化的接口，写入json文件中
    summary_change_list = get_summary_changed_interface_info(old_json_data, new_json_data)
    method_change_list = get_method_changed_interface_info(old_json_data, new_json_data)
    parameter_type_change_list = get_parameter_type_changed_interface_info(old_json_data, new_json_data)
    parameter_change_list = get_parameter_changed_interface_info(old_json_data, new_json_data)
    header_change_list = get_header_changed_interface_info(old_json_data, new_json_data)
    # 获取没有变化的接口列表，没有去除部分信息变化的接口地址
    no_change_list = get_no_changes_interface_info(old_json_data, new_json_data)
    # 合并目前这五大类列表，并去重，只要地址出现在任何一个列表中，都说明这个接口变更了
    all_list = []
    for s in summary_change_list:
        address = list(s.keys())[0]
        all_list.append(address)
    for s in method_change_list:
        address = list(s.keys())[0]
        all_list.append(address)
    for s in parameter_type_change_list:
        address = list(s.keys())[0]
        all_list.append(address)
    for s in parameter_change_list:
        address = list(s.keys())[0]
        all_list.append(address)
    for s in header_change_list:
        address = list(s.keys())[0]
        all_list.append(address)
    # 去重
    all_list = list(set(all_list))
    for address in all_list:
        if address in no_change_list:
            # 去除变更了的地址
            no_change_list.remove(address)
    # 第十六步：复制现有的所有接口的yml文件到用例目录下，注意：若已有用例信息，需要仅变更用例信息的部分数据，而不是全部都被替换
    # 上个版本的用例存放根目录
    old_path = all_cases_gen_path + "/" + old_version
    # 先把新增的接口的yml文件从上个版本的yml文件目录全部复制过来
    if len(new_list) > 0:
        for path in new_list:
            old_0 = new_case_path + path
            copy_all_files(old_0, cases_path, new)
    # 已废弃的接口，目录都不会被创建，所以，直接可以忽略不考虑，无需复制

    # 已删除的接口的目录，也不会被创建，所以，也可以直接忽略这种情况的

    # 再把一切都没有变化的接口的那些yml文件，直接复制过来
    if len(no_change_list) > 0:
        for path in no_change_list:
            old_0 = old_path + path
            copy_all_files(old_0, cases_path, old_version)
    # 最后再把接口地址没有变，但里面的内容有了一些变化的接口的yml文件，只更改yml文件的部分内容，再复制过来
    # 先整体复制过来，再根据具体的变化，修改现有的yml文件，然后再进行保存
    if len(all_list) > 0:
        for path in all_list:
            old_0 = old_path + path
            copy_all_files(old_0, cases_path, old_version)
    # 再根据具体的变化，修改现有的yml文件，然后再进行保存
    if len(method_change_list) > 0:
        for i in range(len(method_change_list)):
            every_path_info = method_change_list[i]
            for key in every_path_info:
                key_value = every_path_info[key]
                new_method = key_value['新版本的接口请求方法']
                new_0 = cases_path + key
                for file_name in list(os.listdir(new_0)):
                    if file_name.endswith(".yml"):
                        yml_file_name = file_name.split(".")[0]
                        yml_data = get_yaml_data(new_0, yml_file_name)
                        yml_data["case_common_info"]["interface_method"] = new_method
                        save_ruamel_data(new_0, yml_file_name, yml_data)
                    else:
                        # print("{}是一个目录".format(file_name))
                        pass
    if len(summary_change_list) > 0:
        for i in range(len(summary_change_list)):
            every_path_info = summary_change_list[i]
            for key in every_path_info:
                key_value = every_path_info[key]
                new_summary = key_value['新版本的接口请求描述']
                new_0 = cases_path + key
                for file_name in list(os.listdir(new_0)):
                    if file_name.endswith(".yml"):
                        yml_file_name = file_name.split(".")[0]
                        yml_data = get_yaml_data(new_0, yml_file_name)
                        yml_data["case_common_info"]["interface_name"] = new_summary
                        save_ruamel_data(new_0, yml_file_name, yml_data)
                    else:
                        # print("{}是一个目录".format(file_name))
                        pass
    if len(parameter_type_change_list) > 0:
        for i in range(len(parameter_type_change_list)):
            every_path_info = parameter_type_change_list[i]
            for key in every_path_info:
                key_value = every_path_info[key]
                new_parameters_type = key_value['新版本的接口请求参数类型']
                new_0 = cases_path + key
                # print(new_0)
                # print(os.listdir(new_0))
                for file_name in list(os.listdir(new_0)):
                    if file_name.endswith(".yml"):
                        yml_file_name = file_name.split(".")[0]
                        # print("yml_file_name", yml_file_name)
                        yml_data = get_yaml_data(new_0, yml_file_name)
                        yml_data["case_common_info"]["interface_parameters_type"] = new_parameters_type
                        save_ruamel_data(new_0, yml_file_name, yml_data)
                    else:
                        # print("{}是一个目录".format(file_name))
                        pass
    if len(header_change_list) > 0:
        for i in range(len(header_change_list)):
            every_path_info = header_change_list[i]
            for key in every_path_info:
                key_value = every_path_info[key]
                new_header = key_value['新版本的接口请求头']
                new_0 = cases_path + key
                for file_name in list(os.listdir(new_0)):
                    if file_name.endswith(".yml"):
                        yml_file_name = file_name.split(".")[0]
                        yml_data = get_yaml_data(new_0, yml_file_name)
                        yml_data["case_common_info"]["interface_headers"] = new_header
                        save_ruamel_data(new_0, yml_file_name, yml_data)
                    else:
                        # print("{}是一个目录".format(file_name))
                        pass
    if len(parameter_change_list) > 0:
        for i in range(len(parameter_change_list)):
            every_path_info = parameter_change_list[i]
            for key in every_path_info:
                key_value = every_path_info[key]
                old_parameter = key_value['老版本的接口请求参数']
                new_parameter = key_value['新版本的接口请求参数']
                new_0 = cases_path + key
                params_dict = {

                }
                for old in old_parameter:
                    if old in new_parameter:
                        params_dict[old] = key_value['老版本的接口请求参数'][old]
                    else:
                        pass
                for new in new_parameter:
                    if new not in old_parameter:
                        params_dict[new] = new_parameter[new]
                    else:
                        params_dict[new] = key_value['新版本的接口请求参数'][new]
                for file_name in list(os.listdir(new_0)):
                    if file_name.endswith(".yml"):
                        yml_file_name = file_name.split(".")[0]
                        new_yml_data = get_yaml_data(new_0, yml_file_name)
                        new_yml_data["case_list"][0]["case_step"]["interface_parameters"] = params_dict
                        save_ruamel_data(new_0, yml_file_name, new_yml_data)
                    else:
                        # print("{}是一个目录".format(file_name))
                        pass


# 生成测试数据文件，此处特指生成SQL文件
create_test_data(cases_path, new, data_path)
