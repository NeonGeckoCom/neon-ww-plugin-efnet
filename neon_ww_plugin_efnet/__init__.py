# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os

from eff_word_net import samples_loc
from eff_word_net.engine import HotwordDetector
from eff_word_net.streams import SimpleMicStream

from ovos_plugin_manager.templates.hotwords import HotWordEngine


class EfficientWordNetWakeWordPlugin(HotWordEngine):
    def __init__(self, hotword="hey_mycroft", config=None, lang="en-us"):
        super().__init__(hotword, config or {}, lang)
        self.model = self.config.get("reference_file")
        if not self.model:
            hotword = hotword.lower().strip()
            if hotword == "alexa":
                self.model = os.path.join(samples_loc, "alexa_ref.json")
            elif hotword == "siri":
                self.model = os.path.join(samples_loc, "siri_ref.json")
            elif hotword == "google":
                self.model = os.path.join(samples_loc, "google_ref.json")
            else:
                raise FileNotFoundError("no reference_file provided for EfficientWordNet")

        self.net = HotwordDetector(
            hotword=hotword,
            reference_file=os.path.expanduser(self.model),
        )
        self.has_found = False
        # TODO figure out how to remove need for self.stream
        self.stream = SimpleMicStream()
        self.stream.start_stream()

    def update(self, chunk):
        # TODO figure out how to feed chunk directly
        # remove need for self.stream
        frame = self.stream.getFrame()
        self.has_found = self.net.checkFrame(frame)

    def found_wake_word(self, frame_data):
        if self.has_found:
            self.has_found = False
            return True
        return False
