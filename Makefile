CLUSTER ?= 10

TEXTS 	 = $(patsubst texts/%.txt,%,$(wildcard texts/*.txt))
GRAPHS	 = $(TEXTS:%=build/graph/%.mcl)
CLUSTERS = $(TEXTS:%=build/cluster/%.mclo)

TEXT	 = texts/$(basename $(@F)).txt
GRAPH	 = build/graph/$(basename $(@F)).mcl

.SECONDARY:
.SECONDEXPANSION:

all: $(CLUSTERS)

clean:
	rm -rf build

# Uses Python3.3 or newer
$(GRAPHS): $$(TEXT)
	@mkdir -p $(@D)
	scripts/makegraph.py $< $@

# Uses MCL, available from http://www.micans.org/mcl/
$(CLUSTERS): $$(GRAPH)
	@mkdir -p $(@D)
	mcl $< --abc -o $@ -I $(CLUSTER)

