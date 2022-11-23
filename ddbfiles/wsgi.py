"""WSGI interface."""

from typing import Union

from flask import Response
from his import Application, authenticated, authorized
from wsgilib import JSON, JSONMessage

from ddbfiles.files import FILES
from ddbfiles.stream import stream

__all__ = ['APPLICATION']


APPLICATION = Application('ddbfiles')
NO_SUCH_FILE = JSONMessage('No such file', status=404)


@APPLICATION.route('/list', methods=['GET'], strict_slashes=False)
@authenticated
@authorized('ddbfiles')
def list_files() -> JSON:
    """Returns the DDB manual."""

    return JSON([{
        name: sorted(dict(file.versions)) for name, file in FILES.items()
    }])


@APPLICATION.route('/<file>/<version>', methods=['GET'], strict_slashes=False)
@authenticated
@authorized('ddbfiles')
def get_file(file: str, version: str) -> Union[JSONMessage, Response]:
    """Returns the DDB manual."""

    try:
        file = FILES[file]
    except KeyError:
        return JSONMessage('No such file.', status=404)

    try:
        path = file.version(version)
    except ValueError:
        return JSONMessage('No such version.', status=404)

    if not path.is_file():
        return JSONMessage('File not found.', status=404)

    return Response(
        stream(path),
        mimetype='application/octet-stream',
        headers={'Content-Disposition': f'filename="{path.name}"'}
    )
