# Eolie

![Eolie logo](https://raw.githubusercontent.com/gnumdk/eolie/master/data/icons/hicolor/256x256/apps/org.gnome.Eolie.png)

Eolie is a new GNOME web browser.

- Adblock helpers (please contribute): https://github.com/gnumdk/eolie-adblock

- For users: http://gnumdk.github.io/eolie-web (not yet)

- FAQ: https://github.com/gnumdk/eolie/wiki

- For translators: https://translate.zanata.org/project/view/eolie

It provides:
- Firefox sync support
- Secret password store
- A modern ui

## Depends on

- gtk3 >= 3.14
- gobject-introspection
- python3
- intltool (make)
- itstool (make)
- python (make)
- python-cairo
- python-dbus
- python-gobject
- python-sqlite
- WebKit2GTK >= 2.16
- Webkit introspection support

## Special python modules
For full support, please install this python modules:
```
# pip3 install requests-hawk PyFxA pycrypto beautifulsoup4 cryptography
```

## For packagers
Full deps here: https://github.com/flathub/org.gnome.Eolie

## Building from git

```
$ git clone https://github.com/gnumdk/eolie.git
$ cd eolie
$ meson build
$ sudo ninja -C build install
```

### On Ubuntu

```
$ git clone https://github.com/gnumdk/eolie.git
$ cd eolie
$ sudo apt-get install autoconf libglib2.0-dev intltool yelp-tools libgirepository1.0-dev libgtk-3-dev python-gobject-dev python3-dev libwebkit2gtk-4.0-dev gir1.2-webkit2-4.0
$ meson build
$ sudo ninja -C build install
```

Instead of `make install` you might want to use `checkinstall`

```
# apt-get install checkinstall
# checkinstall
```

This will allow you to uninstall eolie as a package, for example with `apt-get uninstall eolie`.

### On Fedora

```
$ git clone https://github.com/gnumdk/eolie.git
$ cd eolie
$ sudo dnf install autoconf glib2-devel intltool yelp-tools gtk3-devel gobject-introspection-devel python3 itstool pygobject3-devel python3-devel webkitgtk4-devel
$ meson build
$ sudo ninja -C build install
```
