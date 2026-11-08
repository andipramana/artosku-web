"""Makes assets/qr-play.svg once (static QR to the Play Store listing). Needs: pip install segno. Not used at runtime."""
import segno
URL = 'https://play.google.com/store/apps/details?id=com.artosku'
segno.make(URL, error='m').save('assets/qr-play.svg', border=4, scale=1, dark='#000000', light='#ffffff',
                                xmldecl=False, svgns=True, omitsize=True, nl=False)
