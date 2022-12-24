import flet
from flet import (
    ElevatedButton,
    FilePicker,
    FilePickerResultEvent,
    Page,
    Row,
    Text,
    icons,
)

from pytube import Playlist
from pytube import streams
streams.Stream.do



def main(page: Page):
    directory_path = Text()
    def button_clicked(e,):
        url = url_input.value
        playlist = Playlist(url)
        output_path = directory_path.value
        print('Number of videos in playlist: %s' % len(playlist.video_urls))

        download = lambda id,x: x.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(
            output_path=output_path,
            filename= f'{id+1}_{x.title}'
        )
        for id,x in enumerate(playlist.videos):
            download(id,x)


    page.add(flet.Markdown('# Youtube Playlist Downloader'))
    url_input = flet.TextField(label='Youtube Playlist URL:')
    btn = flet.ElevatedButton(text="Submit", on_click=button_clicked)
    page.add(url_input,Row(
            [
                ElevatedButton(
                    "Choose Output Directory",
                    icon=icons.FOLDER_OPEN,
                    on_click=lambda _: get_directory_dialog.get_directory_path(),
                    disabled=page.web,
                ),
                directory_path,
            ]
        ) ,btn)





    # Pick files dialog
    # def pick_files_result(e: FilePickerResultEvent):
    #     selected_files.value = (
    #         ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
    #     )
    #     selected_files.update()
    #
    # pick_files_dialog = FilePicker(on_result=pick_files_result)
    # selected_files = Text()
    #
    # # Save file dialog
    # def save_file_result(e: FilePickerResultEvent):
    #     save_file_path.value = e.path if e.path else "Cancelled!"
    #     save_file_path.update()
    #
    # save_file_dialog = FilePicker(on_result=save_file_result)
    # save_file_path = Text()

    # Open directory dialog
    def get_directory_result(e: FilePickerResultEvent):
        directory_path.value = e.path if e.path else "Cancelled!"
        directory_path.update()

    get_directory_dialog = FilePicker(on_result=get_directory_result)


    # hide all dialogs in overlay
    page.overlay.extend([get_directory_dialog])




if __name__ == '__main__':
    flet.app(target=main,
             # view=flet.WEB_BROWSER
             )