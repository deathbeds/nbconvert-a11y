import pandas, bs4, functools
from .outputs import repr_semantic


def get_caption(df):
    dl = new("dl", role="presentation")
    dl.append(new("dt", "rows")), dl.append(new("dd", str(len(df))))
    dl.append(new("dt", "columns")), dl.append(new("dd", str(len(df.columns))))
    dl.append(new("dt", "indexes:")), dl.append(
        new("dd", indexes := new("dl", role="presentation"))
    )
    indexes.append(new("dt", "rows")), indexes.append(new("dd", str(df.index.nlevels)))
    indexes.append(new("dt", "columns")), indexes.append(new("dd", str(df.columns.nlevels)))
    return dl


def row_major_at_rows(df):
    return df.columns.nlevels + len(df)


def row_major_at_cols(df):
    return df.index.nlevels + int(any(df.columns.names)) + len(df.columns)


@repr_semantic.register(pandas.Series)
def repr_series(object):
    return get_table(object.to_frame().T)


@repr_semantic.register(pandas.DataFrame)
def get_table(df, caption=None, ARIA=True):
    soup = bs4.BeautifulSoup(features="lxml")
    ROWS, COLS = any(df.index.names), any(df.columns.names)
    WIDE = (df.shape[1] + 1) > pandas.options.display.max_columns
    LONG = (df.shape[0] + 1) > pandas.options.display.max_rows
    col_ranges, row_ranges = get_ranges(df, WIDE, LONG)
    soup.append(
        table := new(
            "table",
            colcount=row_major_at_cols(df) if ARIA or WIDE else None,
            rowcount=row_major_at_rows(df) if ARIA or LONG else None,
        )
    )
    table.append(cap := new("caption", caption))
    cap.append(get_caption(df))
    get_thead(df, table, col_ranges, WIDE, ARIA, LONG)
    get_tbody(df, table, col_ranges, row_ranges, WIDE, ARIA, LONG)
    return soup


def get_thead(df, table, col_ranges, WIDE=False, ARIA=False, LONG=False):
    ROWS, COLS = any(df.index.names), any(df.columns.names)
    col_center = col_ranges[1].start - col_ranges[0].stop
    for col_level, col_name in enumerate(df.columns.names):
        table.append(tr := trow(rowindex=col_level + 1 if ARIA or LONG and row_part else None))
        if not col_level:
            if ROWS or not COLS:
                for row_level, row_name in enumerate(df.index.names):
                    tr.append(
                        th := theading(
                            str(row_name) or f"index {row_level}",
                            scope="col",
                            rowspan=df.columns.nlevels if df.columns.nlevels > 1 else None,
                            colindex=row_level + 1 if ARIA else None,
                        )
                    )
        if COLS:
            tr.append(
                theading(
                    str(col_name) or f"level {col_level}",
                    scope="row",
                    colindex=df.index.nlevels + 1 if ARIA else None,
                )
            )

        for col_part, col_range in enumerate(col_ranges):
            if col_part:
                tr.append(
                    theading(
                        HIDDEN,
                        colindex=(
                            col_index + 2 + df.index.nlevels + bool(LONG and WIDE) if ARIA else None
                        ),
                        **{"aria-colspan": col_center},
                    )
                )
            for col_index in col_range:
                col_value = df.columns.get_level_values(col_level)[col_index]
                tr.append(
                    theading(
                        str(col_value),
                        scope="col",
                        colindex=(
                            df.index.nlevels + int(ROWS and COLS) + col_index + 1
                            if ARIA or WIDE and col_part
                            else None
                        ),
                    )
                )


def get_tbody(df, table, col_ranges, row_ranges, WIDE=False, ARIA=False, LONG=False):
    ROWS, COLS = any(df.index.names), any(df.columns.names)
    row_center = row_ranges[1].start - row_ranges[0].stop
    col_center = col_ranges[1].start - col_ranges[0].stop
    for row_part, row_range in enumerate(row_ranges):
        if row_part:
            table.append(
                tr := trow(
                    rowindex=row_index + 2 + df.columns.nlevels, **{"aria-rowspan": row_center}
                )
            )
            for row_level in range(df.index.nlevels):
                tr.append(theading(HIDDEN, colindex=row_level + 1))
            if ROWS and COLS:
                tr.append(tdata(EMPTY, colindex=row_level + 2))
            for col_part, col_range in enumerate(col_ranges):
                if col_part:
                    tr.append(
                        tdata(
                            HIDDEN,
                            colindex=col_index + 2 + df.index.nlevels + int(ROWS and COLS),
                            **{"aria-rowspan": row_center, "aria-colspan": col_center},
                        ),
                    )
                for col_index in col_range:
                    tr.append(
                        tdata(
                            HIDDEN, colindex=col_index + 1 + df.index.nlevels + int(ROWS and COLS)
                        )
                    )
        for row_index in row_range:
            table.append(tr := trow(rowindex=row_index + 1 + df.columns.nlevels))
            for row_level in range(df.index.nlevels):
                tr.append(
                    theading(
                        str(df.index.get_level_values(row_level)[row_index]),
                        colindex=row_level + 1 if ARIA else None,
                        scope="row",
                    )
                )
            if ROWS and COLS:
                tr.append(tdata(EMPTY, colindex=row_level + 2))
            for col_part, col_range in enumerate(col_ranges):
                if col_part:
                    tr.append(
                        tdata(
                            HIDDEN,
                            colindex=col_index + 2 + df.index.nlevels + int(ROWS and COLS),
                            **{"aria-colspan": col_center},
                        )
                    )
                for col_index in col_range:
                    tr.append(
                        tdata(
                            str(df.iloc[row_index, col_index]),
                            colindex=col_index + 1 + df.index.nlevels + int(ROWS and COLS),
                        )
                    )


def get_frame_bounds(df, WIDE=False, LONG=False):
    a, b, c, d = len(df.columns), len(df.columns), len(df), len(df)
    if WIDE:
        a = pandas.options.display.max_columns // 2
        b -= a
    if LONG:
        c = pandas.options.display.max_rows // 2
        d -= c
    return a, b, c, d


def get_ranges(df, WIDE=False, LONG=False):
    a, b, c, d = get_frame_bounds(df, WIDE=WIDE, LONG=LONG)
    return (range(a), range(b, df.shape[1])), (range(c), range(d, df.shape[0]))


def new(
    tag,
    string=None,
    rowindex=None,
    colindex=None,
    rowcount=None,
    colcount=None,
    rowspan=None,
    colspan=None,
    scope=None,
    *,
    soup=bs4.BeautifulSoup(features="lxml"),
    **attrs,
):
    """create a new beautiful soup with table and aria properties"""
    data = locals()
    attrs.update(
        {
            f"aria-{k}": data.get(k)
            for k in ["rowindex", "colindex", "rowcount", "colcount"]
            if data.get(k)
        }
    )
    attrs.update({k: data.get(k) for k in ["rowspan", "colspan", "scope"] if data.get(k)})
    tag = soup.new_tag(tag, attrs=attrs)
    if string:
        tag.append(string)
    return tag


trow = functools.partial(new, "tr")
theading = functools.partial(new, "th")
tdata = functools.partial(new, "td")

HIDDEN, EMPTY = "hidden", "empty"
