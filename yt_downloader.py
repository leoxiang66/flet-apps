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
from pathlib import Path



from pytube import Playlist







def main(page: Page):
    # Open directory dialog
    def get_directory_result(e: FilePickerResultEvent):
        directory_path.value = e.path if e.path else "Cancelled!"
        directory_path.update()

    def button_clicked(e, ):
        url = url_input.value
        if url is not None and ('https' in url or 'http' in url):
            playlist = Playlist(url)
            number_videos = len(playlist.video_urls)
            print('Number of videos in playlist: %s' % number_videos)

            output_path = directory_path.value

            if output_path is None:
                p = Path(__file__).parent.absolute().joinpath("downloads")
                output_path = p.__str__()
                p.mkdir(parents=True, exist_ok=True)
                directory_path.value = output_path
                page.update()

            download = lambda id, x: x.streams.filter(progressive=True, file_extension='mp4').order_by(
                'resolution').desc().first().download(
                output_path=output_path,
                # filename=str(Path(output_path).joinpath(Path(f'''{id + 1}_{x.title}.mp4''')))
            )

            for id, x in enumerate(playlist.videos):
                print('start downloading...')
                download(id, x)
                pb.value = (id+1) / number_videos
                pb.visible = True
                page.update()

                print(f'downloaded: {x.title}.mp4')

            pb.visible = False

    get_directory_dialog = FilePicker(on_result=get_directory_result)
    directory_path = Text()
    page.overlay.append(get_directory_dialog)
    page.update()
    
    pb = flet.ProgressBar(width=page.width,visible= False)

    page.add(flet.Markdown('# Youtube Playlist Downloader'))
    url_input = flet.TextField(label='Youtube Playlist URL:')
    btn = flet.ElevatedButton(text="Submit", on_click=button_clicked)
    page.add(url_input, Row(
        [
            ElevatedButton(
                "Choose Output Directory",
                icon=icons.FOLDER_OPEN,
                on_click=lambda _: get_directory_dialog.get_directory_path(),
                disabled=page.web,
            ),
            directory_path,
        ]
    ), btn,
             pb
             )
    
    

                        
                    
                














    # hide all dialogs in overlay
    # page.overlay.extend([get_directory_dialog])




if __name__ == '__main__':
    flet.app(target=main,
             # view=flet.WEB_BROWSER
             )