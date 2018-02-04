Scaling Strategies
==================


Architecture
------------

1. Client-logic on client (i.e. Javascript-heavy).
1. Matching the Javascript<->Python data interface (i.e. JSON).
1. API Star server - high-performance w asyncio upgrade option. Python 3.6.
1. Non-HTML static content is served via whitenoise for smooth CDN upgrade path.
1. Database usage favours key lookups, lending to datastores & similar.
1. Abstracted key/value cache behaviour (currently memcache).

Scaling: General
----------------

#### Aggregation of marginal gains

> "1 percent margin for improvement in everything you do."
-Dave Brailsford

#### Network traffic

1. Libraries combined, minified, optimised.
1. Paths shortened.
1. CDN directives on HTML pages.

#### Dashboard

1. Javascript poll time/control can be altered.
1. Memcache cache time can be increased.
1. Implementation of permission tokens (e.g. load-based).

#### Survey

1. Automatic answer-sending can be altered to e.g. onblur only, instead of also onchange.
1. Implementation of captchas to limit front-end abuse attempts.
1. Implementation of permission tokens to limit back-end abuse attempts.


Scaling: Infrastructure & Framework
-----------------------------------

1. Separate (cloud) servers scaled per component, esp. database.
1. Load balancer, multiple web & database servers.
1. Nginx revision/replace. Static content.
1. Async upgrade, sending & receiving data on-the-fly.


Scaling: MySQL Database
-----------------------

1. Hardware
1. Optimised server conf
1. Reduced integer column sizes 
1. Optimised indexes e.g. substr, order
1. INSERT DELAYED & similar
1. Views (native or bespoke)
1. Master/Slave (master for surveys; slaves for dashboards)
1. Clustering
