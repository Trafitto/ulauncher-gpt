from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction

from gpt import GPT
EXTENSION_ICON = 'images/icon.png'


class UlauncherGPTExtension(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []

        gpt_client = GPT(extension.preferences)

        question = event.get_argument()
        if not question:
            return RenderResultListAction([
                ExtensionResultItem(icon=EXTENSION_ICON,
                                    name='Ask something to chatGPT',
                                    on_enter=DoNothingAction())
            ])
        try:
            response = gpt_client.ask(question)
        except Exception as err:
            return RenderResultListAction([
                ExtensionResultItem(icon=EXTENSION_ICON,
                                    name='Error while connecting to OpenAI: ' +
                                    err,
                                    on_enter=CopyToClipboardAction(str(err)))
            ])

        items.append(ExtensionResultItem(icon=EXTENSION_ICON, name="GPT", description=response,
                                         on_enter=CopyToClipboardAction(response)))

        return RenderResultListAction(items)


if __name__ == '__main__':
    UlauncherGPTExtension().run()
