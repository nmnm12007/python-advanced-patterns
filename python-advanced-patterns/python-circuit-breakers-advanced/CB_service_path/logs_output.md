# LOGS

## service_a

python.exe service_a.py

* Serving Flask app 'service_a'
* Debug mode: off
  2025-12-26 08:39:13,689 | INFO | werkzeug | WARNING: This is a development
  server. Do not use it in a production deployment. Use a production WSGI server
  instead.
* Running on http://127.0.0.1:5000
  2025-12-26 08:39:13,690 | INFO | werkzeug | Press CTRL+C to quit
  2025-12-26 08:39:18,994 | INFO | root | DEBUG: state=<
  pybreaker.CircuitClosedState object at 0x0000019EDFFC1D30> |
  current_state=closed | types=<class 'pybreaker.CircuitClosedState'> <class '
  str'>
  2025-12-26 08:39:18,995 | INFO | root | [CALL]: Service
  B :: http://127.0.0.1:5001/process :: CB State:  CircuitClosedState
  2025-12-26 08:39:19,007 | WARNING | circuit_breaker | Retrying
  circuit_breaker.call_service_b in 1.0 seconds as it raised HTTPError: 500
  Server Error: INTERNAL SERVER ERROR for url: http://127.0.0.1:5001/process.
  2025-12-26 08:39:20,009 | INFO | root | DEBUG: state=<
  pybreaker.CircuitClosedState object at 0x0000019EDFFC1D30> |
  current_state=closed | types=<class 'pybreaker.CircuitClosedState'> <class '
  str'>
  2025-12-26 08:39:20,010 | INFO | root | [CALL]: Service
  B :: http://127.0.0.1:5001/process :: CB State:  CircuitClosedState
  2025-12-26 08:39:20,023 | ERROR | root | [DOWNSTREAM FAILURE]
  RetryError[<Future at 0x19edffc7750 state=finished raised HTTPError>]
  2025-12-26 08:39:20,024 | INFO | werkzeug |
  127.0.0.1 - - [26/Dec/2025 08:39:20] "GET /call HTTP/1.1"
  502 -                                                         
  2025-12-26 08:40:05,426 | INFO | root | DEBUG: state=<
  pybreaker.CircuitClosedState object at 0x0000019EDFFC1D30> |
  current_state=closed | types=<class 'pybreaker.CircuitClosedState'> <class '
  str'>
  2025-12-26 08:40:05,426 | INFO | root | [CALL]: Service
  B :: http://127.0.0.1:5001/process :: CB State:  CircuitClosedState
  2025-12-26 08:40:05,434 | WARNING | root | CBListener changed state from <
  pybreaker.CircuitClosedState object at 0x0000019EDFFC1D30> to <
  pybreaker.CircuitOpenState object at 0x0000019EE0035010>
  2025-12-26 08:40:05,434 | WARNING | circuit_breaker | Retrying
  circuit_breaker.call_service_b in 1.0 seconds as it raised
  CircuitBreakerError: Failures threshold reached, circuit breaker opened.
  2025-12-26 08:40:06,435 | ERROR | root | [DOWNSTREAM FAILURE]
  RetryError[<Future at 0x19edffdec40 state=finished raised CircuitBreakerError>]
  2025-12-26 08:40:06,436 | INFO | werkzeug |
  127.0.0.1 - - [26/Dec/2025 08:40:06] "GET /call HTTP/1.1"
  502 -                                                         
  2025-12-26 08:40:37,398 | WARNING | root | CBListener changed state from <
  pybreaker.CircuitOpenState object at 0x0000019EE0035010> to <
  pybreaker.CircuitHalfOpenState object at 0x0000019EE0036510>
  2025-12-26 08:40:37,398 | INFO | root | DEBUG: state=<
  pybreaker.CircuitHalfOpenState object at 0x0000019EE0036510> |
  current_state=half-open | types=<class 'pybreaker.CircuitHalfOpenState'> <
  class 'str'>
  2025-12-26 08:40:37,399 | INFO | root | [CALL]: Service
  B :: http://127.0.0.1:5001/process :: CB State:  CircuitHalfOpenState
  2025-12-26 08:40:37,403 | WARNING | root | CBListener changed state from <
  pybreaker.CircuitHalfOpenState object at 0x0000019EE0036510> to <
  pybreaker.CircuitOpenState object at 0x0000019EE00620D0>
  2025-12-26 08:40:37,404 | WARNING | circuit_breaker | Retrying
  circuit_breaker.call_service_b in 1.0 seconds as it raised
  CircuitBreakerError: Trial call failed, circuit breaker opened.
  2025-12-26 08:40:38,404 | ERROR | root | [DOWNSTREAM FAILURE]
  RetryError[<Future at 0x19ee00485f0 state=finished raised CircuitBreakerError>]
  2025-12-26 08:40:38,405 | INFO | werkzeug |
  127.0.0.1 - - [26/Dec/2025 08:40:38] "GET /call HTTP/1.1"
  502 -                                                         
  2025-12-26 08:40:50,385 | WARNING | root | CBListener changed state from <
  pybreaker.CircuitOpenState object at 0x0000019EE00620D0> to <
  pybreaker.CircuitHalfOpenState object at 0x0000019EE0061F90>
  2025-12-26 08:40:50,386 | INFO | root | DEBUG: state=<
  pybreaker.CircuitHalfOpenState object at 0x0000019EE0061F90> |
  current_state=half-open | types=<class 'pybreaker.CircuitHalfOpenState'> <
  class 'str'>
  2025-12-26 08:40:50,386 | INFO | root | [CALL]: Service
  B :: http://127.0.0.1:5001/process :: CB State:  CircuitHalfOpenState
  2025-12-26 08:40:50,392 | WARNING | root | CBListener changed state from <
  pybreaker.CircuitHalfOpenState object at 0x0000019EE0061F90> to <
  pybreaker.CircuitOpenState object at 0x0000019EE0062350>
  2025-12-26 08:40:50,392 | WARNING | circuit_breaker | Retrying
  circuit_breaker.call_service_b in 1.0 seconds as it raised
  CircuitBreakerError: Trial call failed, circuit breaker opened.
  2025-12-26 08:40:51,393 | ERROR | root | [DOWNSTREAM FAILURE]
  RetryError[<Future at 0x19ee00646b0 state=finished raised CircuitBreakerError>]
  2025-12-26 08:40:51,394 | INFO | werkzeug |
  127.0.0.1 - - [26/Dec/2025 08:40:51] "GET /call HTTP/1.1"
  502 -                                                         
  2025-12-26 08:41:02,992 | WARNING | root | CBListener changed state from <
  pybreaker.CircuitOpenState object at 0x0000019EE0062350> to <
  pybreaker.CircuitHalfOpenState object at 0x0000019EE0061F90>
  2025-12-26 08:41:02,992 | INFO | root | DEBUG: state=<
  pybreaker.CircuitHalfOpenState object at 0x0000019EE0061F90> |
  current_state=half-open | types=<class 'pybreaker.CircuitHalfOpenState'> <
  class 'str'>
  2025-12-26 08:41:02,993 | INFO | root | [CALL]: Service
  B :: http://127.0.0.1:5001/process :: CB State:  CircuitHalfOpenState
  2025-12-26 08:41:02,997 | WARNING | root | CBListener changed state from <
  pybreaker.CircuitHalfOpenState object at 0x0000019EE0061F90> to <
  pybreaker.CircuitClosedState object at 0x0000019EE00625D0>
  2025-12-26 08:41:02,997 | INFO | werkzeug |
  127.0.0.1 - - [26/Dec/2025 08:41:02] "GET /call HTTP/1.1" 200 -
  2025-12-26 08:41:11,928 | INFO | root | DEBUG: state=<
  pybreaker.CircuitClosedState object at 0x0000019EE00625D0> |
  current_state=closed | types=<class 'pybreaker.CircuitClosedState'> <class '
  str'>
  2025-12-26 08:41:11,928 | INFO | root | [CALL]: Service
  B :: http://127.0.0.1:5001/process :: CB State:  CircuitClosedState
  2025-12-26 08:41:11,934 | INFO | werkzeug |
  127.0.0.1 - - [26/Dec/2025 08:41:11] "GET /call HTTP/1.1" 200 -
  2025-12-26 08:45:50,853 | INFO | root | DEBUG: state=<
  pybreaker.CircuitClosedState object at 0x0000019EE00625D0> |
  current_state=closed | types=<class 'pybreaker.CircuitClosedState'> <class '
  str'>
  2025-12-26 08:45:50,853 | INFO | root | [CALL]: Service
  B :: http://127.0.0.1:5001/process :: CB State:  CircuitClosedState
  2025-12-26 08:45:50,858 | INFO | werkzeug |
  127.0.0.1 - - [26/Dec/2025 08:45:50] "GET /call HTTP/1.1" 200 -

## service_b

python service_b.py

* Serving Flask app 'service_b'
* Debug mode: off
  WARNING: This is a development server. Do not use it in a production
  deployment. Use a production WSGI server instead.
* Running on http://127.0.0.1:5001
  Press CTRL+C to quit
  127.0.0.1 - - [26/Dec/2025 08:39:19] "GET /process HTTP/1.1" 500 -
  127.0.0.1 - - [26/Dec/2025 08:39:20] "GET /process HTTP/1.1" 500 -
  127.0.0.1 - - [26/Dec/2025 08:40:05] "GET /process HTTP/1.1" 500 -
  127.0.0.1 - - [26/Dec/2025 08:40:37] "GET /process HTTP/1.1" 500 -
  127.0.0.1 - - [26/Dec/2025 08:40:50] "GET /process HTTP/1.1" 500 -
  127.0.0.1 - - [26/Dec/2025 08:41:02] "GET /process HTTP/1.1" 200 -
  127.0.0.1 - - [26/Dec/2025 08:41:11] "GET /process HTTP/1.1" 200 -
  127.0.0.1 - - [26/Dec/2025 08:45:50] "GET /process HTTP/1.1" 200 -
