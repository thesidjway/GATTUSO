# /usr/bin/env python
import yaml
import os
import sys

class Params:
	def __init__(self):
		self.package_name = "my_pkg"
		self.class_name = "MyPkg"
		self.lib_name = "MyPkg"
		self.pkg_version = "0.1.1"
		self.pkg_description = "My Package"
		self.maintainer_email = "siddharthjha@outlook.com"
		self.maintainer_name = "Siddharth Jha"
		self.ros = True
		self.opencv = True
		self.gtsam = True
		self.ceres = True
		self.pcl = True
		self.eigen = True
		self.ros_pkgs = ["roscpp", "rospy", "std_msgs", "geometry_msgs"]
		self.cmake_minimum_req = "2.8.3"
		self.cpp_version = "11"
		self.year = "2019"
		self.package_name_full = "My Package"
		self.node_object = "mpn"

def gen_cmakelists(params):
	f = open("CMakeLists.txt","w+")
	f.write("cmake_minimum_required(VERSION " + params.cmake_minimum_req + ")\n")
	f.write("project(" + params.package_name + ")\n\n")
	f.write("set(CMAKE_CXX_STANDARD " + params.cpp_version + ")\n\n")
	if params.ros:
		f.write("find_package(catkin REQUIRED COMPONENTS")
		for i in params.ros_pkgs:
			f.write(" "+i)
		f.write(")\n\n")

	if params.eigen:
		f.write("find_package (Eigen3 REQUIRED)\n")
	if params.opencv:
		f.write("find_package (OpenCV REQUIRED)\n")
	if params.pcl:
		f.write("find_package (PCL REQUIRED COMPONENTS common io) \n")
	if params.ceres:
		f.write("find_package (Ceres REQUIRED) \n")
	if params.gtsam:
		f.write("find_package (GTSAM REQUIRED)\n")

	f.write("\ninclude_directories(\n")
	f.write("\t\tinclude/\n")
	if params.eigen:
		f.write("\t\tEigen\n")
	if params.ros:
		f.write("\t\t${catkin_INCLUDE_DIRS}\n")
	if params.opencv:
		f.write("\t\t${OpenCV_INCLUDE_DIRS}\n")
	f.write(")\n")

	if params.ros:
		f.write("\ncatkin_package(\n")
		f.write("\tINCLUDE_DIRS include\n")
		f.write("\tLIBRARIES " + params.package_name + "\n")
		f.write("\tCATKIN DEPENDS")
		for i in params.ros_pkgs:
			f.write(" " + i)
		f.write("\n)\n\n")
	f.write("add_executable(")
	f.write(params.package_name + "_node src/" + params.package_name + "_node.cc src/" + params.class_name + ".cc")
	f.write(")\n")
	f.write("target_link_libraries(" + params.package_name + "_node")
	if params.ros:
		f.write(" ${catkin_LIBRARIES}")
	if params.ceres:
		f.write(" ceres")
	if params.opencv:
		f.write(" ${OpenCV_LIBRARIES}")
	if params.gtsam:
		f.write(" gtsam gtsam_unstable")
	if params.pcl:
		f.write(" ${PCL_COMMON_LIBRARIES} ${PCL_IO_LIBRARIES}")
	f.write(")\n")

def constdest(params, name, f):
	f.write(name + "::" + name + "() {\n")
	f.write("}\n\n")
	f.write(name + "::~" + name + "() {\n")
	f.write("}\n\n")


def add_license(params, f):
	license_txt = "/*\n\t" + params.package_name_full + "\n\tCopyright (C) " +  params.year +  " " + params.maintainer_name + """\n\tThis program is free software; you can redistribute it and/or
	modify it under the terms of the GNU General Public License
	as published by the Free Software Foundation; either version 2
	of the License, or (at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program; if not, write to the Free Software
	Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n*/\n"""
	f.write(license_txt)

def gen_package_xml(params):
	f = open("package.xml","w+")
	f.write('<?xml version="1.0"?>\n<package>\n')
	f.write("\t<name>" + params.package_name + "</name>\n")
	f.write("\t<version>" + params.pkg_version + "</version>\n")
	f.write("\t<description>" + params.pkg_description + "</description>\n\n")
	f.write('"\t<maintainer email="' + params.maintainer_email + '">' + params.maintainer_name + "</maintainer>\n\n")
	f.write("\t<license>BSD</license>\n\n")
	f.write("\t<buildtool_depend>catkin</buildtool_depend>\n")
	for i in params.ros_pkgs:
		f.write("\t<build_depend>" + i + "</build_depend>\n")
	for i in params.ros_pkgs:
		f.write("\t<run_depend>" + i + "</run_depend>\n")
	f.write("\n\t<export>\n")
	f.write("\t</export>\n\n")
	f.write("</package>")

def intmain(params, s):
	s.write("int main(int argc, char** argv) {\n")
	s.write("\t" + params.package_name + "_node " + params.node_object + ";\n")
	if params.ros:
		s.write("\tros::init(argc, argv, " + '"params.package_name"' + ");\n")
		s.write("\t" + params.node_object + ".initCallbacks();\n")
	s.write("}")

def gen_node(params, path_orig):
	pathsrc = os.path.join(path_orig, "src")
	pathincprev = os.path.join(path_orig, "include")
	pathinc = os.path.join(pathincprev, params.package_name)
	os.chdir(pathsrc)
	s = open(params.package_name + "_node.cc","w+")
	add_license(params, s)
	s.write("#include <" + params.package_name + "/" + params.package_name + "_node.h>\n\n")
	constdest(params, params.package_name + "_node", s)
	if params.ros:
		s.write("void " + params.package_name + "_node::initCallbacks() {\n")
		s.write("}\n\n")
	intmain(params, s)
	os.chdir(pathinc)
	i = open(params.package_name + "_node.h","w+")
	add_license(params, i)
	i.write("#pragma once\n\n")
	if params.ros:
		i.write("#include <ros/ros.h>\n")
	i.write("#include <" + params.package_name + "/" + params.class_name + ".h>\n\n")
	i.write("class " + params.package_name + "_node {\n")
	i.write("private:\n")
	if params.ros:
		i.write("\tros::NodeHandle nh_;\n")
	i.write("public:\n")
	i.write("\t"+params.package_name+"_node();\n")
	i.write("\t~"+params.package_name+"_node();\n")
	if params.ros:
		i.write("\tvoid initCallbacks();\n")
	i.write("};\n")

def gen_cpp(params, path_orig):
	pathsrc = os.path.join(path_orig, "src")
	pathincprev = os.path.join(path_orig, "include")
	pathinc = os.path.join(pathincprev, params.package_name)
	os.chdir(pathsrc)
	s = open(params.class_name + ".cc","w+")
	add_license(params, s)
	s.write("#include <" + params.package_name + "/" + params.class_name + ".h>\n\n")
	constdest(params, params.class_name, s)
	os.chdir(pathinc)
	i = open(params.class_name + ".h","w+")
	add_license(params, i)
	i.write("#pragma once\n\n")
	i.write("class " + params.class_name + " {\n")
	i.write("private:\n")
	i.write("public:\n")
	i.write("\t"+params.class_name+"();\n")
	i.write("\t~"+params.class_name+"();\n")
	i.write("};\n")

def read_params(config_file):
	params_ = Params()
	fil = yaml.load(open(config_file))
	params_.package_name = fil['package_name']
	params_.class_name = fil['class_name']
	params_.lib_name = fil['lib_name']
	params_.pkg_version = fil['pkg_version']
	params_.pkg_description = fil['pkg_description']
	params_.maintainer_email = fil['maintainer_email']
	params_.maintainer_name = fil['maintainer_name']
	params_.ros = fil['ros']
	params_.opencv = fil['opencv']
	params_.gtsam = fil['gtsam']
	params_.ceres = fil['ceres']
	params_.pcl = fil['pcl']
	params_.eigen = fil['eigen']
	params_.ros_pkgs = fil['ros_pkgs']
	params_.cmake_minimum_req = fil['cmake_minimum_req']
	params_.cpp_version = fil['cpp_version']
	params_.year = fil['year']
	params_.package_name_full = fil['package_name_full']
	params_.node_object = fil['node_object']
	return params_


if __name__ == "__main__":
	if len(sys.argv) is not 2:
		print "Invalid syntax. Usage: python gattuso.py config.yaml"
		exit()
	params = read_params(sys.argv[1])
	path = os.path.join(os.getcwd(), params.package_name)
	path_orig = path
	if not os.path.exists(path):
		os.mkdir(path)
	os.chdir(path)
	path = os.path.join(os.getcwd(), "src")
	if not os.path.exists(path):
		os.mkdir(path)
	path = os.path.join(os.getcwd(), "include")
	if not os.path.exists(path):
		os.mkdir(path)
		os.chdir(path)
		path = os.path.join(os.getcwd(), params.package_name)
		if not os.path.exists(path):
			os.mkdir(path)
	os.chdir(path_orig)
	gen_cmakelists(params)
	if params.ros:
		gen_package_xml(params)
	gen_node(params, path_orig)
	gen_cpp(params, path_orig)