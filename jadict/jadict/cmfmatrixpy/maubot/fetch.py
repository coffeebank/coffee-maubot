
async def maubot_fetch_image(self, image_url: str, mime_type: str="image/jpg", filename: str="image.jpg"):
    """Fetch and upload an image to Matrix using Maubot"""
    resp = await self.http.get(image_url)
    if resp.status != 200:
        return None
    og_image = await resp.read()
    mxc = await self.client.upload_media(og_image, mime_type=mime_type, filename=filename)
    return mxc
