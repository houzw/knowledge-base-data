#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: houzhiwei
# time: 2019/9/5 9:03
import re


class Preprocessor(object):

	@staticmethod
	def remove_bracket_content(content):
		"""
		删除括号内部的内容
		Args:
			content:

		Returns:

		"""
		content = re.sub("\([a-zA-Z0-9 *\-]+\)", " ", content)
		content = re.sub("[ ]+", " ", content)
		return content.strip()

	@staticmethod
	def remove_parenthesis(string):
		"""
		remove parenthesis | 移除小括号
		Returns:

		"""
		return string.replace('(', '').replace(')', '')

	@staticmethod
	def normalize(remove_str, content):
		if content is None:
			content = ''
		else:
			content = re.sub(remove_str, '', content).strip()
		return content

	@staticmethod
	def replace_2_space(replace_regex, content):
		content = re.sub(replace_regex, ' ', content)
		content = re.sub("[ ]+", ' ', content).strip()
		return content

	@staticmethod
	def replace_2_underline(replace_regex, content):
		content = re.sub(replace_regex, ' ', content)
		content = Preprocessor.space_2_underline(content)
		return content

	@staticmethod
	def space_2_underline(content: str):
		if content:
			content = re.sub("[ ]+", ' ', content).strip()
			content = content.replace(' ', '_')
			content = re.sub("[_]{2,}", '_', content)
		return content

	@staticmethod
	def task_name(name: str):
		name += '_task'
		# 有问题
		name = re.sub("\([a-zA-Z0-9*_ /\-]+\)", '', name).strip()
		return name

	@staticmethod
	def name_underline(name: str):
		name = re.sub("\[[()a-zA-Z0-9*^,.\- /]+\]", '', name.lower()).strip()
		name = re.sub("\([a-zA-Z0-9* /]+\)", '', name).strip()
		return name.replace(" ", "_").replace('_-_', '_')

	@staticmethod
	def toolname_underline(name: str):
		name = re.sub('[()*&\[\]\']', '', name)
		name = re.sub('[ /]+', '_', name)
		name = re.sub('( - )', '-', name)
		name = re.sub('[.](2,3)', '', name)
		name = re.sub('[_,]+', '_', name)
		name = re.sub('_-_', '_', name).strip()
		name = re.sub("^[Tt](ool)[_0-9: ]+", '', name).strip()
		return name

	@staticmethod
	def to_upper_camel_case(name, space: bool):
		"""
		convert space or underline splited string to camelcase string
		Args:
			name:
			space: is separated by space or underline

		Returns:

		"""
		if space:
			tokens = [token.capitalize() for token in str(name).split(" ")]
			return ''.join(tokens)
		else:
			tokens = [token.capitalize() for token in str(name).split("_")]
			return ''.join(tokens)
