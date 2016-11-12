import ast
from collections import deque
from ast_helper import *
from Call import Call 

class ASTFuncDef(object):

    def __init__(self, node):
        self.node = node
        self.name = node.name
        self.calls = self.dfs_walk_get_calls(node)

    def __str__(self):
        print self.name
 
    # Walks through function and returns linkedlist of calls.
    def dfs_walk_get_calls(self, node):
        return self.dfs_walk_body([node])

    # Walks through if statements and returns head of children 
    def dfs_walk_ifs(self, node):
        children = []
        while True:
            body = node.body
            children.append(self.dfs_walk_body(body)) # first if
            if isinstance(node.orelse[0], ast.If):
                node = node.orelse[0]
            else:
                children.append(self.dfs_walk_body(node.orelse))
                break
        return children

    # Walks through body and 
    def dfs_walk_body(self, todo):
        todo = deque(todo)
        latest_calls = [Call(None)]
        first_call = None
        while todo:
            node = todo.popleft()
            if isinstance(node, ast.If):
                children = self.dfs_walk_ifs(node)
                for child in children:
                    for latest_call in latest_calls:
                        latest_call.add_child(child)
                        child.add_parent(latest_call)
                latest_calls = [child.get_tails() for child in children]
#                print "if", latest_calls
                child_nodes = None
            elif isinstance(node, ast.Call):
                current_call = Call(node)
                if first_call is None:
                    first_call = current_call
#                print latest_calls
                for latest_call in latest_calls: 
                    latest_call.add_child(current_call)
                    current_call.add_parent(latest_call)
                latest_calls = [current_call]
#                print "call", [latest_call.name for latest_call in latest_calls]
                child_nodes = None
            else:
                child_nodes = iter_child_nodes(node)
                child_nodes.reverse()
            if child_nodes is not None:
                todo.extendleft(child_nodes)
        return first_call

