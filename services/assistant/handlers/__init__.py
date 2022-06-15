"""
Command handlers.
"""


# class TikTokVideoDownloadCommandHandler(ChainOfResponsibility):
#     def process_request(self, request: CommandRequest) -> bool:
#         link = extract_tiktok_link(request.message)
#         if not link:
#             return False
#
#         post = TikTokVideo(link)
#         download_and_send_post.delay(request.chat_id, post.id)
#         logger.info(f'downloading TikTok post: {link}')
#
#         return True
