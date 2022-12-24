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
    directory_path = Text()
    file_picker = flet.FilePicker()
    page.overlay.append(file_picker)
    page.update()
    
    pb = flet.ProgressBar(width=page.width,visible= False)
    
    
    def button_clicked(e,):
        url = url_input.value
        if url is not None and ('https' in url or 'http' in url):
            playlist = Playlist(url)
            number_videos = len(playlist.video_urls)
            print('Number of videos in playlist: %s' % number_videos)
        
            output_path = directory_path.value
            
            if output_path is None:
                output_path = './downloads'
                p = Path(output_path)
                p.mkdir(parents=True, exist_ok=True)
                directory_path.value = str(p.absolute())
                page.update()
                        
                    
                


            download = lambda id,x: x.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(
                output_path=output_path,
                filename= f'{id+1}_{x.title}.mp4'
            )
            
            for id,x in enumerate(playlist.videos):
                download(id,x)
                pb.value = id / number_videos
                pb.visible = True
                page.update()
            
            pb.visible = False


    page.add(flet.Markdown('# Youtube Playlist Downloader'))
    url_input = flet.TextField(label='Youtube Playlist URL:')
    btn = flet.ElevatedButton(text="Submit", on_click=button_clicked)
    page.add(url_input,Row(
            [
                ElevatedButton(
                    "Choose Output Directory",
                    icon=icons.FOLDER_OPEN,
                    on_click=lambda _: file_picker.get_directory_path(),
                    disabled=page.web,
                ),
                directory_path,
            ]
        ) ,btn,
             pb
             )



    # Open directory dialog
    def get_directory_result(e: FilePickerResultEvent):
        directory_path.value = e.path if e.path else "Cancelled!"
        directory_path.update()

    get_directory_dialog = FilePicker(on_result=get_directory_result)


    # hide all dialogs in overlay
    # page.overlay.extend([get_directory_dialog])




if __name__ == '__main__':
    flet.app(target=main,
             # view=flet.WEB_BROWSER
             )