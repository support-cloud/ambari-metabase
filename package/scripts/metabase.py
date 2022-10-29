# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from resource_management.core.exceptions import ExecutionFailed, ComponentIsNotRunning
from resource_management.core.resources.system import Execute
from resource_management.libraries.script.script import Script

from common import metabaseHome, metabaseJarUrl, startCmdTmpl


class Metabase(Script):
    def install(self, env):
        Execute('mkdir -p {0}'.format(metabaseHome))
        Execute('cd {0} && wget {1} '.format(metabaseHome, metabaseJarUrl))

    def stop(self, env):
        Execute("ps -ef |grep -v grep | grep 'jar metabase.jar'|awk '{print $2}' |xargs kill -9 ")

    def start(self, env):
        jvmArgs = self.configure(env)
        startCmd = startCmdTmpl.format(jvmArgs)
        Execute('cd {0} && nohup {1} > out.metabase 2>&1 & '.format(metabaseHome, startCmd))

    def status(self, env):
        #TODO
        try:
            Execute(
                'export CNT=`ps -ef |grep -v grep |grep "jar metabase.jar" | wc -l` && `if [ $CNT -ne 0 ];then exit '
                '0;else exit 3;fi ` '
            )
        except ExecutionFailed as ef:
            if ef.code == 3:
                raise ComponentIsNotRunning("ComponentIsNotRunning")
            else:
                raise ef

    def configure(self, env):
        from params import metabaseConfig
        jvmArgs = ' '
        for key, value in metabaseConfig.iteritems():
            jvmArgs += '-D' + key + '="' + value + '" '
        return jvmArgs


if __name__ == '__main__':
    Metabase().execute()
