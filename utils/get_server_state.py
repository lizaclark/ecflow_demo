import ecflow
import ctypes
import tempfile
from cStringIO import StringIO
import sys
import contextlib
import os
import io

#class Capturing(list):
#    def __enter__(self):
#        self._stdout = sys.stdout
#        sys.stdout = self._stringio = StringIO()
#        return self
#    def __exit__(self, *args):
#        self.extend(self._stringio.getvalue().splitlines())
#        sys.stdout = self._stdout

libc = ctypes.CDLL(None)
c_stdout = ctypes.c_void_p.in_dll(libc, 'stdout')

@contextlib.contextmanager
def stdout_redirector(stream):
    # The original fd stdout points to. Usually 1 on POSIX systems.
    original_stdout_fd = sys.stdout.fileno()

    def _redirect_stdout(to_fd):
        """Redirect stdout to the given file descriptor."""
        # Flush the C-level buffer stdout
        libc.fflush(c_stdout)
        # Flush and close sys.stdout - also closes the file descriptor (fd)
        sys.stdout.close()
        # Make original_stdout_fd point to the same file as to_fd
        os.dup2(to_fd, original_stdout_fd)
        # Create a new sys.stdout that points to the redirected fd
        sys.stdout = io.TextIOWrapper(os.fdopen(original_stdout_fd, 'wb'))

    # Save a copy of the original stdout fd in saved_stdout_fd
    saved_stdout_fd = os.dup(original_stdout_fd)
    try:
        # Create a temporary file and redirect stdout to it
        tfile = tempfile.TemporaryFile(mode='w+b')
        _redirect_stdout(tfile.fileno())
        # Yield to caller, then redirect stdout back to the saved fd
        yield
        _redirect_stdout(saved_stdout_fd)
        # Copy contents of temporary file to the given stream
        tfile.flush()
        tfile.seek(0, io.SEEK_SET)
        stream.write(tfile.read())
    finally:
        tfile.close()
        os.close(saved_stdout_fd)

try:
    ci = ecflow.Client()
    ci.stats()
    f = io.BytesIO()
    with stdout_redirector(f): 
        ci.stats()
    #with Capturing() as output:
    #    ci.stats()
except RuntimeError, e:
    print str(e)

print "output of stats"
print f.getvalue().decode('utf-8')
