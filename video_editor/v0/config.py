class Config:
    def __init__(self):
        self.pre_processed_videos = './data/videos/pre_processed_clips/'
        self.processed_clips = './data/videos/processed_clips/'
        self.audio_directory = './data/audio/'
        self.output_directory = './output/'
        self.codec="libx264"
        self.audio_codec="aac"

        self.testingMode = True 
        self.fps=30
        self.threads = 8   
        self.audio_start_time = 0
        self.clips_duration = 5

        self.final_video_duration = 12
        self.final_videos_beat_sync = 3 # videos beat algo
        self.final_videos_offset_sync = 3 # videos offset algo
        self.minimum_clip_duration = 0.5 # seconds

        # self.text = "This will be the text"
        # self.text_placement = "center" # top, bottom, ...
        # self.text_family = ""
        # self.reuse_clips = True # default 
        # self.crossfade_duration = 0.5

        # other cool video stuff

        # Fastest path to revenue 
        # what if people can get reels for $1? 
        # website emails us videos
        # we pass into generator and generate clips manually
        # email or text final reels to customer 

        # Within next month 
        # Setup AWS so they can generate reels anytime 


    # are these reels worth $1 yet? 
    # How to get around the music legal issue? Delegate this to lawyer? 
    # What would make these reels wayy better? understood busness? like what? 
        # * branding for fonts and color scheme
        # * templates to tell them what to make? 
        # * does insta/capcut/tiktok do this already? if so how can we be 10X better.

    
    # finish webscraping tonight 
    # messag