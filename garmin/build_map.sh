#!/bin/bash

TEMP_DIR=temp
BOUNDS=bounds-latest.zip
SEA=sea-latest.zip
MKGMAP=mkgmap
SPLITTER=mkgmap-splitter

FAMILY_ID="6324" # mkgmap default
PRODUCT_ID=1

CODEPAGE=1251

TEMPLATE_ARGS="$TEMP_DIR/template.args"
MKGMAP_ARGS=""

mkdir -p $TEMP_DIR
rm -rf $TEMP_DIR/*

usage() {
	echo "Usage: $0 <options>" >&2
	echo "Required args:" >&2
	echo "  -i <input.pbf>	Input file" >&2
	echo "  -o <output.img>	Output file" >&2

	echo "Options:" >&2
	echo "  -s <style>		Path to mkgmap style" >&2
	echo "  -t <TYP file>		Path to TYP file" >&2
	echo "  -c <country>		Country name" >&2
	echo "  -k <country code>	Country code, 2-symbols" >&2
	echo "  -d <description>	Map description" >&2
	echo "  -y <copyright>	Copyright text" >&2
	echo "  -f <family>		Map Family ID" >&2
	echo "  -n <family name>	Family name" >&2
	echo "  -e <series name>	Series name" >&2
	echo "  -C <codepage>		Codepage (1251 by default)" >&2
	echo "  -m <mkgmap>		Command to run mkgmap [default: mkgmap]" >&2
	echo "  -S <splitter>		Command to run splitter [default: mkgmap-splitter]" >&2
	echo "  -v			Verbose output" >&2

	exit 1
}

while getopts "ho:i:f:s:t:c:k:y:n:e:m:S:d:C:" arg; do
	case "${arg}" in
		h)
			usage ;;
		i)
			INPUT_FILE="${OPTARG}" ;;
		o)
			OUTPUT_FILE="${OPTARG}" ;;
		f)
			FAMILY_ID="${OPTARG}" ;;
		s)
			MKGMAP_ARGS="$MKGMAP_ARGS --style-file='${OPTARG}'" ;;
		t)
			TYP_FILE="${OPTARG}" ;;
		c)
			MKGMAP_ARGS="$MKGMAP_ARGS --country-name='${OPTARG}'" ;;
		k)
			MKGMAP_ARGS="$MKGMAP_ARGS --country-abbr='${OPTARG}'" ;;
		y)
			MKGMAP_ARGS="$MKGMAP_ARGS --copyright-message='${OPTARG}'" ;;
		d)
			MKGMAP_ARGS="$MKGMAP_ARGS --description='${OPTARG}'" ;;
		n)
			MKGMAP_ARGS="$MKGMAP_ARGS --family-name='${OPTARG}'" ;;
		e)
			MKGMAP_ARGS="$MKGMAP_ARGS --series-name='${OPTARG}'" ;;
		C)
			CODEPAGE=$OPTARG ;;
		v)
			MKGMAP_ARGS="$MKGMAP_ARGS --verbose --report-roundabout-issues=all" ;;
		m)
			MKGMAP="${OPTARG}" ;;
		S)
			SPLITTER="${OPTARG}" ;;

		*)
			usage ;;
	esac
done

if [ -z "$INPUT_FILE" ]; then
	echo "Input file is not defined" >&2
	usage
fi

if [ -z "$OUTPUT_FILE" ]; then
	echo "Output file is not defined" >&2
	usage
fi

echo "Input:		$INPUT_FILE"
echo "Output file:	$OUTPUT_FILE"
echo "TYP file:		$TYP_FILE"
echo "Family:		$FAMILY_ID"
echo "Additional options:	$MKGMAP_ARGS"

set -e

MAPNAME=${FAMILY_ID}0001

echo "Run splitter for $INPUT_FILE..."
$SPLITTER \
    --precomp-sea="$SEA" \
    --max-nodes=1200000 \
    --keep-complete=true \
    --output=pbf \
    --output-dir="$TEMP_DIR" \
    --mapid=$MAPNAME \
    "$INPUT_FILE" > "$TEMP_DIR/splitter.log"

echo "Run mkgmap..."
eval $MKGMAP \
    --output-dir="$TEMP_DIR" \
    --tdbfile \
    --code-page=$CODEPAGE \
    --lower-case \
    --name-tag-list=name,name:ru,name:be,int_name \
    --remove-short-arcs \
    --drive-on=right \
    --mapname=$MAPNAME \
    --family-id=$FAMILY_ID \
    --product-id=$PRODUCT_ID \
    --make-poi-index \
    --index \
	--nsis \
    --poi-address \
    --route \
    --draw-priority=31 \
    --bounds="$BOUNDS" \
    --precomp-sea="$SEA" \
    --housenumbers \
    --add-pois-to-areas \
    --gmapi \
    --gmapsupp \
    $MKGMAP_ARGS \
    -c "$TEMPLATE_ARGS"  "$TYP_FILE"

echo "Done, copying result to $OUTPUT_FILE"

cd "$TEMP_DIR"
gmap_dir=`echo *.gmap`
gmap_tgz=`basename "${OUTPUT_FILE%%.img}.gmap.tgz"`
tar czf "$gmap_tgz" "$gmap_dir"
cd ..

mv "$TEMP_DIR/gmapsupp.img" "$OUTPUT_FILE"
mv "$TEMP_DIR/$gmap_tgz" "`dirname \"$OUTPUT_FILE\"`"
rm -rf temp/*


