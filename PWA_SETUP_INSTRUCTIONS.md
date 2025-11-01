# PWA Setup Instructions

## Icons Required

The PWA requires two icon files to be placed in `accounts/static/`:

1. **icon-192x192.png** - 192x192 pixels
2. **icon-512x512.png** - 512x512 pixels

### Creating Icons

You can create these icons using:

1. **Online Tools:**
   - [RealFaviconGenerator](https://realfavicongenerator.net/)
   - [PWA Asset Generator](https://github.com/elegantapp/pwa-asset-generator)

2. **Design Requirements:**
   - Icon should represent "Apartment Management"
   - Use colors matching the site theme: Purple (#9D6DC2, #5A2D82) and Orange (#FFA719, #FFCD7B)
   - Ensure icons work on both light and dark backgrounds (maskable icons)

3. **Quick Generate:**
   ```bash
   # If you have Node.js installed:
   npm install -g pwa-asset-generator
   pwa-asset-generator your-icon.png accounts/static/ --icon-only
   ```

4. **Manual Creation:**
   - Create a square image with your logo/icon
   - Resize to 192x192 and 512x512
   - Save as PNG with transparency
   - Place in `accounts/static/` folder

## PWA Features Implemented

✅ **Offline Access**
- Service worker caches all static assets
- HTML pages use stale-while-revalidate strategy
- API calls use network-first with cache fallback

✅ **Offline Data Storage**
- IndexedDB stores offline-created data for:
  - Apartments
  - Units
  - Tenants
  - Payments
  - Bills
  - Other Charges

✅ **Automatic Sync**
- Data syncs automatically when connection is restored
- Syncs on page load if online
- Background sync support

✅ **Installability**
- Web app manifest configured
- Install prompt for supported browsers
- Standalone display mode

✅ **Offline Indicator**
- Shows when device is offline
- Shows count of pending items to sync
- Updates in real-time

## Testing the PWA

### 1. Test Offline Functionality
```bash
# In Chrome DevTools:
# 1. Open DevTools (F12)
# 2. Go to Application tab
# 3. Service Workers section - verify service worker is registered
# 4. Check Cache Storage - verify assets are cached
# 5. Check IndexedDB - verify data structure
# 6. Network tab - check "Offline" checkbox
# 7. Try navigating - should load from cache
```

### 2. Test Installation
- **Desktop (Chrome/Edge):** Look for install icon in address bar
- **Mobile (Android):** "Add to Home Screen" prompt
- **Mobile (iOS):** Share button → "Add to Home Screen"

### 3. Test Data Sync
1. Go offline (use DevTools Network tab)
2. Create/edit some data (apartment, tenant, payment, etc.)
3. Data should be saved to IndexedDB
4. Go back online
5. Data should sync automatically
6. Page should reload to show synced data

### 4. Lighthouse Audit
```bash
# Run Lighthouse in Chrome DevTools:
# 1. Open DevTools
# 2. Go to Lighthouse tab
# 3. Select "Progressive Web App"
# 4. Click "Analyze page load"
# 5. Should score 90+ on PWA audit
```

## Troubleshooting

### Service Worker Not Registering
- Check browser console for errors
- Verify `service-worker.js` is accessible at `/static/service-worker.js`
- Check that HTTPS is used (or localhost for development)

### Icons Not Showing
- Verify icons exist in `accounts/static/`
- Run `python manage.py collectstatic`
- Clear browser cache and service worker
- Check manifest.json icon paths

### Data Not Syncing
- Check browser console for IndexedDB errors
- Verify CSRF token is available
- Check network requests in DevTools
- Ensure API endpoints are correct

### Offline Indicator Not Showing
- Check browser console for JavaScript errors
- Verify `db.js` is loaded correctly
- Check that `updateOfflineIndicator()` is called

## Next Steps After Icon Creation

1. Place icons in `accounts/static/`:
   ```
   accounts/static/icon-192x192.png
   accounts/static/icon-512x512.png
   ```

2. Collect static files:
   ```bash
   python manage.py collectstatic --noinput
   ```

3. Restart Django server:
   ```bash
   python manage.py runserver
   ```

4. Test the PWA:
   - Open in browser
   - Check service worker registration in console
   - Test offline mode
   - Test installation

## Additional Notes

- Service worker updates automatically when files change
- Cache version increments to force update (change CACHE_NAME in service-worker.js)
- IndexedDB structure is versioned (DB_VERSION in db.js)
- All offline data is stored locally until sync succeeds

