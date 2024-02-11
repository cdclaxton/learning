<mxfile host="Chrome" modified="2024-02-11T13:18:59.748Z" agent="Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" version="21.2.7" etag="iUqPeI2M647ZDcgGB1-d" type="device">
  <diagram id="s3ajqU6_hN6JOdqz-PYY" name="Page-1">
    <mxGraphModel dx="1922" dy="1136" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1654" pageHeight="1169" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-189" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=none;dashed=1;" vertex="1" parent="1">
          <mxGeometry x="40" y="860" width="1600" height="280" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-154" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#B3B3B3;" vertex="1" parent="1">
          <mxGeometry x="920" y="650" width="480" height="180" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-39" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=none;dashed=1;" vertex="1" parent="1">
          <mxGeometry x="30.000000000000007" y="395" width="458.75" height="370" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-36" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFCC;dashed=1;" vertex="1" parent="1">
          <mxGeometry x="320" y="20" width="750" height="230" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-1" value="&lt;b&gt;Input&lt;/b&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;" vertex="1" parent="1">
          <mxGeometry x="30" y="20" width="60" height="30" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-4" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="Gxz8XZ3srZawtTpm0HoM-2" target="Gxz8XZ3srZawtTpm0HoM-3">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-2" value="&lt;font style=&quot;font-size: 10px;&quot; face=&quot;Courier New&quot;&gt;{&lt;br&gt;&lt;font color=&quot;#0066cc&quot;&gt;&quot;text&quot;&lt;/font&gt;: &lt;font color=&quot;#00994d&quot;&gt;&quot;The warehouse is located at 12 Straight Street, London near the docks&quot;&lt;/font&gt;, &lt;br&gt;&lt;font color=&quot;#0066cc&quot;&gt;&quot;threshold&quot;:&lt;/font&gt; 0.5, &lt;br&gt;&lt;font color=&quot;#0066cc&quot;&gt;&quot;min_tokens_to_check&quot;&lt;/font&gt;: 2&lt;br&gt;}&lt;/font&gt;" style="text;html=1;strokeColor=#666666;fillColor=#f5f5f5;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;spacing=2;spacingLeft=5;spacingRight=5;fontColor=#333333;" vertex="1" parent="1">
          <mxGeometry x="30" y="50" width="260" height="110" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-3" value="Tokenise, convert to lowercase, remove punctuation" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="350" y="75" width="120" height="60" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-5" value="Feed tokens in entity matchers" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="530" y="75" width="120" height="60" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-6" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;" edge="1" parent="1" source="Gxz8XZ3srZawtTpm0HoM-3" target="Gxz8XZ3srZawtTpm0HoM-5">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="500" y="160" as="sourcePoint" />
            <mxPoint x="360" y="115" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-7" value="Sort results in descending order of probability" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="720" y="75" width="120" height="60" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-8" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;" edge="1" parent="1" source="Gxz8XZ3srZawtTpm0HoM-5" target="Gxz8XZ3srZawtTpm0HoM-7">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="480" y="115" as="sourcePoint" />
            <mxPoint x="540" y="115" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-9" value="Find the most likely entity matches" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="720" y="170" width="120" height="60" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-10" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;" edge="1" parent="1" source="Gxz8XZ3srZawtTpm0HoM-7" target="Gxz8XZ3srZawtTpm0HoM-9">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="660" y="115" as="sourcePoint" />
            <mxPoint x="730" y="115" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-12" value="&lt;b&gt;Output&lt;/b&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;" vertex="1" parent="1">
          <mxGeometry x="1100" y="20" width="60" height="30" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-13" value="&lt;font style=&quot;font-size: 10px;&quot; face=&quot;Courier New&quot;&gt;{&lt;br&gt;&lt;font color=&quot;#0066cc&quot;&gt;&quot;matches&quot;&lt;/font&gt;: [ ... ], &lt;br&gt;&lt;font color=&quot;#0066cc&quot;&gt;&quot;most_likely_matches&quot;:&lt;/font&gt; [ ... ], &lt;br&gt;&lt;font color=&quot;#0066cc&quot;&gt;&quot;num_results&quot;&lt;/font&gt;: 10,&lt;br&gt;&lt;/font&gt;&lt;font style=&quot;border-color: var(--border-color); font-family: &amp;quot;Courier New&amp;quot;; font-size: 10px;&quot; color=&quot;#0066cc&quot;&gt;&quot;message&quot;&lt;/font&gt;: &lt;font color=&quot;#00994d&quot;&gt;&quot;success&quot;&lt;/font&gt;,&lt;font style=&quot;font-size: 10px;&quot; face=&quot;Courier New&quot;&gt;&lt;br&gt;}&lt;/font&gt;" style="text;html=1;strokeColor=#666666;fillColor=#f5f5f5;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;spacing=2;spacingLeft=5;spacingRight=5;fontColor=#333333;" vertex="1" parent="1">
          <mxGeometry x="1100" y="50" width="210" height="110" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-14" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;" edge="1" parent="1" source="Gxz8XZ3srZawtTpm0HoM-7" target="Gxz8XZ3srZawtTpm0HoM-15">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="850" y="160" as="sourcePoint" />
            <mxPoint x="730" y="115" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-15" value="Generate JSON response" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="920" y="75" width="120" height="60" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-16" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.5;entryY=1;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;" edge="1" parent="1" source="Gxz8XZ3srZawtTpm0HoM-9" target="Gxz8XZ3srZawtTpm0HoM-15">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="790" y="145" as="sourcePoint" />
            <mxPoint x="790" y="180" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-17" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;" edge="1" parent="1" source="Gxz8XZ3srZawtTpm0HoM-15" target="Gxz8XZ3srZawtTpm0HoM-13">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="1060" y="50" as="sourcePoint" />
            <mxPoint x="930" y="115" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-18" value="" style="strokeWidth=2;html=1;shape=mxgraph.flowchart.database;whiteSpace=wrap;" vertex="1" parent="1">
          <mxGeometry x="103.75" y="300" width="50" height="60" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-19" value="External database, e.g. MySQL database containing addresses running in Docker" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;" vertex="1" parent="1">
          <mxGeometry x="163.13" y="305" width="147.5" height="50" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-20" value="Generate entity and token lookup database" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="68.75" y="485" width="120" height="60" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-22" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;exitPerimeter=0;" edge="1" parent="1" source="Gxz8XZ3srZawtTpm0HoM-18" target="Gxz8XZ3srZawtTpm0HoM-20">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="168.75" y="270" as="sourcePoint" />
            <mxPoint x="228.75" y="270" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-23" value="" style="strokeWidth=2;html=1;shape=mxgraph.flowchart.database;whiteSpace=wrap;" vertex="1" parent="1">
          <mxGeometry x="293.13" y="485" width="50" height="60" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-24" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;entryPerimeter=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;" edge="1" parent="1" source="Gxz8XZ3srZawtTpm0HoM-20" target="Gxz8XZ3srZawtTpm0HoM-23">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="233.13" y="515" as="sourcePoint" />
            <mxPoint x="143.13" y="525" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-25" value="Sqlite database" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;" vertex="1" parent="1">
          <mxGeometry x="273.76" y="455" width="88.75" height="30" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-33" style="edgeStyle=none;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=0;exitDx=0;exitDy=0;entryX=0;entryY=0.85;entryDx=0;entryDy=0;entryPerimeter=0;endArrow=none;endFill=0;dashed=1;dashPattern=1 1;" edge="1" parent="1" source="Gxz8XZ3srZawtTpm0HoM-27" target="Gxz8XZ3srZawtTpm0HoM-23">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-27" value="" style="shape=internalStorage;whiteSpace=wrap;html=1;backgroundOutline=1;" vertex="1" parent="1">
          <mxGeometry x="163.13" y="615" width="80" height="80" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-28" value="Maximum number of tokens table" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;" vertex="1" parent="1">
          <mxGeometry x="158.75" y="705" width="88.75" height="40" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-29" value="" style="shape=internalStorage;whiteSpace=wrap;html=1;backgroundOutline=1;" vertex="1" parent="1">
          <mxGeometry x="273.76" y="615" width="80" height="80" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-30" value="Entity ID to tokens table" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;" vertex="1" parent="1">
          <mxGeometry x="269.39" y="705" width="88.75" height="40" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-31" value="" style="shape=internalStorage;whiteSpace=wrap;html=1;backgroundOutline=1;" vertex="1" parent="1">
          <mxGeometry x="383.13" y="615" width="80" height="80" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-32" value="Token to entity ID table" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;" vertex="1" parent="1">
          <mxGeometry x="374.38" y="705" width="88.75" height="40" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-34" style="edgeStyle=none;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=0;exitDx=0;exitDy=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;entryPerimeter=0;endArrow=none;endFill=0;dashed=1;dashPattern=1 1;" edge="1" parent="1" source="Gxz8XZ3srZawtTpm0HoM-29" target="Gxz8XZ3srZawtTpm0HoM-23">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="213.13" y="625" as="sourcePoint" />
            <mxPoint x="303.13" y="546" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-35" style="edgeStyle=none;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=0;exitDx=0;exitDy=0;entryX=1;entryY=0.85;entryDx=0;entryDy=0;entryPerimeter=0;endArrow=none;endFill=0;dashed=1;dashPattern=1 1;" edge="1" parent="1" source="Gxz8XZ3srZawtTpm0HoM-31" target="Gxz8XZ3srZawtTpm0HoM-23">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="223.13" y="635" as="sourcePoint" />
            <mxPoint x="313.13" y="556" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-37" value="&lt;b&gt;Web service&lt;/b&gt; (&lt;font face=&quot;Courier New&quot;&gt;service.py&lt;/font&gt;)" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;" vertex="1" parent="1">
          <mxGeometry x="326.26" y="20" width="180" height="30" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-40" value="&lt;b&gt;Preparation step (&lt;/b&gt;&lt;font face=&quot;Courier New&quot;&gt;00_build_lookup_from_db.py&lt;/font&gt;)" style="text;html=1;strokeColor=none;fillColor=none;align=right;verticalAlign=middle;whiteSpace=wrap;rounded=0;" vertex="1" parent="1">
          <mxGeometry x="188.75" y="405" width="285.01" height="40" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-42" value="&lt;font face=&quot;Courier New&quot;&gt;the&lt;/font&gt;" style="rounded=0;whiteSpace=wrap;html=1;opacity=50;textOpacity=50;" vertex="1" parent="1">
          <mxGeometry x="680" y="310" width="80" height="40" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-43" value="&lt;font face=&quot;Courier New&quot;&gt;warehouse&lt;/font&gt;" style="rounded=0;whiteSpace=wrap;html=1;opacity=50;textOpacity=50;" vertex="1" parent="1">
          <mxGeometry x="760" y="310" width="80" height="40" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-44" value="&lt;font face=&quot;Courier New&quot;&gt;is&lt;/font&gt;" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="840" y="310" width="80" height="40" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-45" value="&lt;font face=&quot;Courier New&quot;&gt;located&lt;/font&gt;" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="920" y="310" width="80" height="40" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-46" value="&lt;font face=&quot;Courier New&quot;&gt;at&lt;/font&gt;" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="1000" y="310" width="80" height="40" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-47" value="&lt;font face=&quot;Courier New&quot;&gt;12&lt;/font&gt;" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="1080" y="310" width="80" height="40" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-48" value="&lt;font face=&quot;Courier New&quot;&gt;straight&lt;/font&gt;" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="1160" y="310" width="80" height="40" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-49" value="&lt;font face=&quot;Courier New&quot;&gt;street&lt;/font&gt;" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="1240" y="310" width="80" height="40" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-50" value="&lt;font face=&quot;Courier New&quot;&gt;london&lt;/font&gt;" style="rounded=0;whiteSpace=wrap;html=1;opacity=50;textOpacity=60;" vertex="1" parent="1">
          <mxGeometry x="1320" y="310" width="80" height="40" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-51" value="&lt;font face=&quot;Courier New&quot;&gt;near&lt;/font&gt;" style="rounded=0;whiteSpace=wrap;html=1;opacity=50;textOpacity=60;" vertex="1" parent="1">
          <mxGeometry x="1400" y="310" width="80" height="40" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-53" value="&lt;font face=&quot;Courier New&quot;&gt;the&lt;/font&gt;" style="rounded=0;whiteSpace=wrap;html=1;opacity=50;textOpacity=60;" vertex="1" parent="1">
          <mxGeometry x="1480" y="310" width="80" height="40" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-54" value="&lt;font face=&quot;Courier New&quot;&gt;docks&lt;/font&gt;" style="rounded=0;whiteSpace=wrap;html=1;opacity=50;textOpacity=60;" vertex="1" parent="1">
          <mxGeometry x="1560" y="310" width="80" height="40" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-67" value="" style="group;fontSize=4;" vertex="1" connectable="0" parent="1">
          <mxGeometry x="330" y="170" width="240" height="10" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-55" value="&lt;font face=&quot;Courier New&quot; style=&quot;font-size: 4px;&quot;&gt;the&lt;/font&gt;" style="rounded=0;whiteSpace=wrap;html=1;fontSize=4;" vertex="1" parent="Gxz8XZ3srZawtTpm0HoM-67">
          <mxGeometry width="19.999999999999996" height="10" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-56" value="&lt;font face=&quot;Courier New&quot; style=&quot;font-size: 4px;&quot;&gt;warehouse&lt;/font&gt;" style="rounded=0;whiteSpace=wrap;html=1;fontSize=4;" vertex="1" parent="Gxz8XZ3srZawtTpm0HoM-67">
          <mxGeometry x="19.999999999999996" width="19.999999999999996" height="10" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-57" value="&lt;font face=&quot;Courier New&quot; style=&quot;font-size: 4px;&quot;&gt;is&lt;/font&gt;" style="rounded=0;whiteSpace=wrap;html=1;fontSize=4;" vertex="1" parent="Gxz8XZ3srZawtTpm0HoM-67">
          <mxGeometry x="39.99999999999999" width="19.999999999999996" height="10" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-58" value="&lt;font face=&quot;Courier New&quot; style=&quot;font-size: 4px;&quot;&gt;located&lt;/font&gt;" style="rounded=0;whiteSpace=wrap;html=1;fontSize=4;" vertex="1" parent="Gxz8XZ3srZawtTpm0HoM-67">
          <mxGeometry x="59.99999999999999" width="19.999999999999996" height="10" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-59" value="&lt;font face=&quot;Courier New&quot; style=&quot;font-size: 4px;&quot;&gt;at&lt;/font&gt;" style="rounded=0;whiteSpace=wrap;html=1;fontSize=4;" vertex="1" parent="Gxz8XZ3srZawtTpm0HoM-67">
          <mxGeometry x="79.99999999999999" width="19.999999999999996" height="10" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-60" value="&lt;font face=&quot;Courier New&quot; style=&quot;font-size: 4px;&quot;&gt;12&lt;/font&gt;" style="rounded=0;whiteSpace=wrap;html=1;fontSize=4;" vertex="1" parent="Gxz8XZ3srZawtTpm0HoM-67">
          <mxGeometry x="99.99999999999999" width="19.999999999999996" height="10" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-61" value="&lt;font face=&quot;Courier New&quot; style=&quot;font-size: 4px;&quot;&gt;straight&lt;/font&gt;" style="rounded=0;whiteSpace=wrap;html=1;fontSize=4;" vertex="1" parent="Gxz8XZ3srZawtTpm0HoM-67">
          <mxGeometry x="119.99999999999999" width="19.999999999999996" height="10" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-62" value="&lt;font face=&quot;Courier New&quot; style=&quot;font-size: 4px;&quot;&gt;street&lt;/font&gt;" style="rounded=0;whiteSpace=wrap;html=1;fontSize=4;" vertex="1" parent="Gxz8XZ3srZawtTpm0HoM-67">
          <mxGeometry x="139.99999999999997" width="19.999999999999996" height="10" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-63" value="&lt;font face=&quot;Courier New&quot; style=&quot;font-size: 4px;&quot;&gt;london&lt;/font&gt;" style="rounded=0;whiteSpace=wrap;html=1;fontSize=4;" vertex="1" parent="Gxz8XZ3srZawtTpm0HoM-67">
          <mxGeometry x="159.99999999999997" width="19.999999999999996" height="10" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-64" value="&lt;font face=&quot;Courier New&quot; style=&quot;font-size: 4px;&quot;&gt;near&lt;/font&gt;" style="rounded=0;whiteSpace=wrap;html=1;fontSize=4;" vertex="1" parent="Gxz8XZ3srZawtTpm0HoM-67">
          <mxGeometry x="180" width="19.999999999999996" height="10" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-65" value="&lt;font face=&quot;Courier New&quot; style=&quot;font-size: 4px;&quot;&gt;the&lt;/font&gt;" style="rounded=0;whiteSpace=wrap;html=1;fontSize=4;" vertex="1" parent="Gxz8XZ3srZawtTpm0HoM-67">
          <mxGeometry x="199.99999999999997" width="19.999999999999996" height="10" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-66" value="&lt;font face=&quot;Courier New&quot; style=&quot;font-size: 4px;&quot;&gt;docks&lt;/font&gt;" style="rounded=0;whiteSpace=wrap;html=1;fontSize=4;" vertex="1" parent="Gxz8XZ3srZawtTpm0HoM-67">
          <mxGeometry x="219.99999999999997" width="19.999999999999996" height="10" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-71" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0;entryDx=0;entryDy=0;exitX=0.5;exitY=1;exitDx=0;exitDy=0;endArrow=none;endFill=0;dashed=1;dashPattern=1 2;strokeColor=#666666;" edge="1" parent="1" source="Gxz8XZ3srZawtTpm0HoM-3" target="Gxz8XZ3srZawtTpm0HoM-61">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="480" y="115" as="sourcePoint" />
            <mxPoint x="540" y="115" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-72" value="&lt;font face=&quot;Courier New&quot;&gt;the&lt;/font&gt;" style="rounded=0;whiteSpace=wrap;html=1;textOpacity=50;opacity=50;" vertex="1" parent="1">
          <mxGeometry x="680" y="590" width="80" height="40" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-73" value="&lt;font face=&quot;Courier New&quot;&gt;warehouse&lt;/font&gt;" style="rounded=0;whiteSpace=wrap;html=1;textOpacity=50;opacity=50;" vertex="1" parent="1">
          <mxGeometry x="760" y="590" width="80" height="40" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-74" value="&lt;font face=&quot;Courier New&quot;&gt;is&lt;/font&gt;" style="rounded=0;whiteSpace=wrap;html=1;textOpacity=50;opacity=50;" vertex="1" parent="1">
          <mxGeometry x="840" y="590" width="80" height="40" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-75" value="&lt;font face=&quot;Courier New&quot;&gt;located&lt;/font&gt;" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="920" y="590" width="80" height="40" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-76" value="&lt;font face=&quot;Courier New&quot;&gt;at&lt;/font&gt;" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="1000" y="590" width="80" height="40" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-77" value="&lt;font face=&quot;Courier New&quot;&gt;12&lt;/font&gt;" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="1080" y="590" width="80" height="40" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-78" value="&lt;font face=&quot;Courier New&quot;&gt;straight&lt;/font&gt;" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="1160" y="590" width="80" height="40" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-79" value="&lt;font face=&quot;Courier New&quot;&gt;street&lt;/font&gt;" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="1240" y="590" width="80" height="40" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-80" value="&lt;font face=&quot;Courier New&quot;&gt;london&lt;/font&gt;" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="1320" y="590" width="80" height="40" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-81" value="&lt;font face=&quot;Courier New&quot;&gt;near&lt;/font&gt;" style="rounded=0;whiteSpace=wrap;html=1;textOpacity=50;opacity=50;" vertex="1" parent="1">
          <mxGeometry x="1400" y="590" width="80" height="40" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-82" value="&lt;font face=&quot;Courier New&quot;&gt;the&lt;/font&gt;" style="rounded=0;whiteSpace=wrap;html=1;textOpacity=50;opacity=50;" vertex="1" parent="1">
          <mxGeometry x="1480" y="590" width="80" height="40" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-83" value="&lt;font face=&quot;Courier New&quot;&gt;docks&lt;/font&gt;" style="rounded=0;whiteSpace=wrap;html=1;textOpacity=50;opacity=50;" vertex="1" parent="1">
          <mxGeometry x="1560" y="590" width="80" height="40" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-85" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#0066CC;strokeWidth=7;" vertex="1" parent="1">
          <mxGeometry x="830" y="300" width="500" height="60" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-86" value="" style="shape=flexArrow;endArrow=classic;html=1;rounded=0;fillColor=#f5f5f5;strokeColor=#666666;" edge="1" parent="1">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="1080" y="380" as="sourcePoint" />
            <mxPoint x="1160" y="440" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-87" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#0066CC;strokeWidth=7;" vertex="1" parent="1">
          <mxGeometry x="910" y="580" width="500" height="60" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-88" value="Sliding window" style="text;html=1;strokeColor=none;fillColor=none;align=right;verticalAlign=middle;whiteSpace=wrap;rounded=0;" vertex="1" parent="1">
          <mxGeometry x="1240" y="270" width="90" height="30" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-94" value="" style="endArrow=none;html=1;rounded=0;strokeWidth=2;" edge="1" parent="1">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="1239.66" y="550" as="sourcePoint" />
            <mxPoint x="1399.66" y="550" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-95" value="" style="endArrow=none;html=1;rounded=0;strokeWidth=2;" edge="1" parent="1">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="1399.66" y="560" as="sourcePoint" />
            <mxPoint x="1399.66" y="550" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-96" value="" style="endArrow=none;html=1;rounded=0;strokeWidth=2;" edge="1" parent="1">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="1239.66" y="560" as="sourcePoint" />
            <mxPoint x="1239.66" y="550" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-97" value="" style="endArrow=none;html=1;rounded=0;strokeWidth=2;" edge="1" parent="1">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="1160" y="530" as="sourcePoint" />
            <mxPoint x="1399.41" y="530" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-98" value="" style="endArrow=none;html=1;rounded=0;strokeWidth=2;" edge="1" parent="1">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="1399.41" y="540" as="sourcePoint" />
            <mxPoint x="1399.41" y="530" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-99" value="" style="endArrow=none;html=1;rounded=0;strokeWidth=2;" edge="1" parent="1">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="1160" y="540" as="sourcePoint" />
            <mxPoint x="1160" y="530" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-100" value="" style="endArrow=none;html=1;rounded=0;strokeWidth=3;strokeColor=#00CC00;" edge="1" parent="1">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="1080" y="510" as="sourcePoint" />
            <mxPoint x="1399.5500000000002" y="510" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-101" value="" style="endArrow=none;html=1;rounded=0;strokeWidth=3;strokeColor=#00CC00;" edge="1" parent="1">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="1399.5500000000002" y="520" as="sourcePoint" />
            <mxPoint x="1399.5500000000002" y="510" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-102" value="" style="endArrow=none;html=1;rounded=0;strokeWidth=3;strokeColor=#00CC00;" edge="1" parent="1">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="1080" y="520" as="sourcePoint" />
            <mxPoint x="1080" y="510" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-103" value="" style="endArrow=none;html=1;rounded=0;strokeWidth=2;" edge="1" parent="1">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="1000" y="490" as="sourcePoint" />
            <mxPoint x="1399.5500000000002" y="490" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-104" value="" style="endArrow=none;html=1;rounded=0;strokeWidth=2;" edge="1" parent="1">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="1399.5500000000002" y="500" as="sourcePoint" />
            <mxPoint x="1399.5500000000002" y="490" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-105" value="" style="endArrow=none;html=1;rounded=0;strokeWidth=2;" edge="1" parent="1">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="1000" y="500" as="sourcePoint" />
            <mxPoint x="1000" y="490" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-106" value="" style="endArrow=none;html=1;rounded=0;strokeWidth=2;" edge="1" parent="1">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="920" y="470" as="sourcePoint" />
            <mxPoint x="1399.2000000000003" y="470" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-107" value="" style="endArrow=none;html=1;rounded=0;strokeWidth=2;" edge="1" parent="1">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="1399.2000000000003" y="480" as="sourcePoint" />
            <mxPoint x="1399.2000000000003" y="470" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-108" value="" style="endArrow=none;html=1;rounded=0;strokeWidth=2;" edge="1" parent="1">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="920" y="480" as="sourcePoint" />
            <mxPoint x="920" y="470" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-109" value="Sub-windows" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;" vertex="1" parent="1">
          <mxGeometry x="1410" y="500" width="100" height="30" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-110" value="&lt;font face=&quot;Courier New&quot;&gt;103&lt;/font&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;" vertex="1" parent="1">
          <mxGeometry x="1330" y="760" width="60" height="20" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-111" value="" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="1330" y="680" width="60" height="20" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-112" value="" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="1330" y="700" width="60" height="20" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-113" value="" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="1330" y="720" width="60" height="20" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-115" value="" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="1330" y="660" width="60" height="20" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-116" value="" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="1330" y="780" width="60" height="20" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-117" value="" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="1330" y="800" width="60" height="20" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-118" value="Entities that contain the token" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;rounded=0;" vertex="1" parent="1">
          <mxGeometry x="1410" y="715" width="100" height="30" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-119" value="&lt;font face=&quot;Courier New&quot;&gt;103&lt;/font&gt;" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;" vertex="1" parent="1">
          <mxGeometry x="1250" y="740" width="60" height="20" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-120" value="" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="1250" y="680" width="60" height="20" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-122" value="210" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;fontColor=#333333;" vertex="1" parent="1">
          <mxGeometry x="1250" y="720" width="60" height="20" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-124" value="" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="1250" y="660" width="60" height="20" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-125" value="" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="1250" y="760" width="60" height="20" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-128" value="103" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;" vertex="1" parent="1">
          <mxGeometry x="1170" y="680" width="60" height="20" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-129" value="" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="1170" y="720" width="60" height="20" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-131" value="" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="1170" y="660" width="60" height="20" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-132" value="210" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;fontColor=#333333;" vertex="1" parent="1">
          <mxGeometry x="1170" y="740" width="60" height="20" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-133" value="" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="1250" y="700" width="60" height="20" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-134" value="" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="1330" y="740" width="60" height="20" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-135" value="" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="1170" y="700" width="60" height="20" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-137" value="" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="1090" y="720" width="60" height="20" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-138" value="" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="1090" y="660" width="60" height="20" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-139" value="" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="1090" y="740" width="60" height="20" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-140" value="210" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;fontColor=#333333;" vertex="1" parent="1">
          <mxGeometry x="1090" y="700" width="60" height="20" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-141" value="103" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;" vertex="1" parent="1">
          <mxGeometry x="1090" y="760" width="60" height="20" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-142" value="" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="1090" y="780" width="60" height="20" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-143" value="" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="1090" y="680" width="60" height="20" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-146" value="" style="rounded=0;whiteSpace=wrap;html=1;" vertex="1" parent="1">
          <mxGeometry x="1010" y="660" width="60" height="20" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-156" value="Get entities for each token" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="640" y="710" width="120" height="60" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-157" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=1;entryY=0.5;entryDx=0;entryDy=0;exitX=0;exitY=0.5;exitDx=0;exitDy=0;" edge="1" parent="1" source="Gxz8XZ3srZawtTpm0HoM-156" target="Gxz8XZ3srZawtTpm0HoM-31">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="339" y="720" as="sourcePoint" />
            <mxPoint x="443" y="720" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-158" value="Read (with an LRU cache)" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;" vertex="1" parent="1">
          <mxGeometry x="545.63" y="665" width="88.75" height="30" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-159" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="Gxz8XZ3srZawtTpm0HoM-156" target="Gxz8XZ3srZawtTpm0HoM-154">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="717" y="720" as="sourcePoint" />
            <mxPoint x="890" y="730" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-160" value="Are the tokens in the sub-window in the correct sequence for the entity?" style="strokeWidth=2;html=1;shape=mxgraph.flowchart.decision;whiteSpace=wrap;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="373.13" y="1010" width="210" height="110" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-162" value="Get the entity&#39;s tokens from the database" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="206.26" y="1035" width="120" height="60" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-163" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=0.25;exitY=0;exitDx=0;exitDy=0;endArrow=none;endFill=0;dashed=1;dashPattern=1 1;" edge="1" parent="1" source="Gxz8XZ3srZawtTpm0HoM-162" target="Gxz8XZ3srZawtTpm0HoM-29">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="717" y="720" as="sourcePoint" />
            <mxPoint x="593" y="820" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-164" value="Read (with an LRU cache)" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;" vertex="1" parent="1">
          <mxGeometry x="261.25" y="800" width="88.75" height="30" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-165" value="Calculate the proportion of tokens in the sub-window that are in the entity" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="640" y="1035" width="120" height="60" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-166" value="Calculate the likelihood" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="820" y="1035" width="120" height="60" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-167" value="Is the likelihood above the required threshold?" style="strokeWidth=2;html=1;shape=mxgraph.flowchart.decision;whiteSpace=wrap;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="1000" y="1010" width="210" height="110" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-168" value="Start" style="strokeWidth=2;html=1;shape=mxgraph.flowchart.start_2;whiteSpace=wrap;" vertex="1" parent="1">
          <mxGeometry x="63.13" y="1015" width="100" height="100" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-169" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;exitPerimeter=0;" edge="1" parent="1" source="Gxz8XZ3srZawtTpm0HoM-168" target="Gxz8XZ3srZawtTpm0HoM-162">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="770" y="710" as="sourcePoint" />
            <mxPoint x="593" y="730" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-170" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;entryPerimeter=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;" edge="1" parent="1" source="Gxz8XZ3srZawtTpm0HoM-162" target="Gxz8XZ3srZawtTpm0HoM-160">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="350" y="1090" as="sourcePoint" />
            <mxPoint x="216" y="1075" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-171" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;exitPerimeter=0;" edge="1" parent="1" source="Gxz8XZ3srZawtTpm0HoM-160" target="Gxz8XZ3srZawtTpm0HoM-165">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="336" y="1075" as="sourcePoint" />
            <mxPoint x="423" y="1075" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-172" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;" edge="1" parent="1" source="Gxz8XZ3srZawtTpm0HoM-165" target="Gxz8XZ3srZawtTpm0HoM-166">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="860" y="1040" as="sourcePoint" />
            <mxPoint x="900" y="1090" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-173" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;entryPerimeter=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;" edge="1" parent="1" source="Gxz8XZ3srZawtTpm0HoM-166" target="Gxz8XZ3srZawtTpm0HoM-167">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="1060" y="1110" as="sourcePoint" />
            <mxPoint x="930" y="1075" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-176" value="Store the probabilistic match" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
          <mxGeometry x="1310" y="1035" width="120" height="60" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-177" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;exitPerimeter=0;" edge="1" parent="1" source="Gxz8XZ3srZawtTpm0HoM-167" target="Gxz8XZ3srZawtTpm0HoM-176">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="1230" y="1100" as="sourcePoint" />
            <mxPoint x="1010" y="1075" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-178" value="True" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;" vertex="1" parent="1">
          <mxGeometry x="581.25" y="1065" width="58.75" height="30" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-179" value="True" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;" vertex="1" parent="1">
          <mxGeometry x="1230" y="1065" width="58.75" height="30" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-181" value="End" style="strokeWidth=2;html=1;shape=mxgraph.flowchart.terminator;whiteSpace=wrap;" vertex="1" parent="1">
          <mxGeometry x="1450" y="900" width="100" height="60" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-182" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0.5;entryY=1;entryDx=0;entryDy=0;entryPerimeter=0;exitX=1;exitY=0.5;exitDx=0;exitDy=0;edgeStyle=orthogonalEdgeStyle;" edge="1" parent="1" source="Gxz8XZ3srZawtTpm0HoM-176" target="Gxz8XZ3srZawtTpm0HoM-181">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="950" y="1075" as="sourcePoint" />
            <mxPoint x="1010" y="1075" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-184" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;entryX=0;entryY=0.5;entryDx=0;entryDy=0;entryPerimeter=0;exitX=0.5;exitY=0;exitDx=0;exitDy=0;edgeStyle=orthogonalEdgeStyle;exitPerimeter=0;" edge="1" parent="1" source="Gxz8XZ3srZawtTpm0HoM-160" target="Gxz8XZ3srZawtTpm0HoM-181">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="1400" y="1075" as="sourcePoint" />
            <mxPoint x="1510" y="990" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-185" value="False" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;" vertex="1" parent="1">
          <mxGeometry x="473.76" y="955" width="58.75" height="30" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-186" style="rounded=0;orthogonalLoop=1;jettySize=auto;html=1;edgeStyle=orthogonalEdgeStyle;entryX=0.11;entryY=0.89;entryDx=0;entryDy=0;entryPerimeter=0;exitX=0.5;exitY=0;exitDx=0;exitDy=0;exitPerimeter=0;" edge="1" parent="1" source="Gxz8XZ3srZawtTpm0HoM-167" target="Gxz8XZ3srZawtTpm0HoM-181">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="890" y="980" as="sourcePoint" />
            <mxPoint x="1430" y="980" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-187" value="False" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;" vertex="1" parent="1">
          <mxGeometry x="1100" y="985" width="58.75" height="30" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-190" value="&lt;b&gt;For each entity in the sub-window that is common to all tokens&lt;/b&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=right;verticalAlign=middle;whiteSpace=wrap;rounded=0;" vertex="1" parent="1">
          <mxGeometry x="1240" y="860" width="375.01" height="30" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-193" value="103" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;" vertex="1" parent="1">
          <mxGeometry x="138.75" y="975" width="60" height="20" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-194" value="e.g. for entity" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;" vertex="1" parent="1">
          <mxGeometry x="50" y="970" width="88.75" height="30" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-197" value="All sub-windows are checked for each window" style="ellipse;shape=cloud;whiteSpace=wrap;html=1;fillColor=none;fontColor=#333333;strokeColor=#666666;spacingLeft=20;spacingRight=10;spacingTop=8;" vertex="1" parent="1">
          <mxGeometry x="1470" y="420" width="165" height="100" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-213" value="" style="group" vertex="1" connectable="0" parent="1">
          <mxGeometry x="796.875" y="937.5" width="143.125" height="95" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-203" value="&lt;font style=&quot;font-size: 8px;&quot;&gt;1&lt;/font&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;" vertex="1" parent="Gxz8XZ3srZawtTpm0HoM-213">
          <mxGeometry x="3.125" y="5" width="30" height="25" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-200" value="" style="endArrow=block;html=1;rounded=0;endFill=1;fillColor=#f5f5f5;strokeColor=#666666;" edge="1" parent="Gxz8XZ3srZawtTpm0HoM-213">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="33.125" y="80" as="sourcePoint" />
            <mxPoint x="33.125" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-201" value="" style="endArrow=block;html=1;rounded=0;endFill=1;fillColor=#f5f5f5;strokeColor=#666666;" edge="1" parent="Gxz8XZ3srZawtTpm0HoM-213">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="23.125" y="70" as="sourcePoint" />
            <mxPoint x="143.125" y="70" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-202" value="" style="endArrow=none;html=1;rounded=0;fillColor=#f5f5f5;strokeColor=#666666;" edge="1" parent="Gxz8XZ3srZawtTpm0HoM-213">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="23.125" y="20" as="sourcePoint" />
            <mxPoint x="33.125" y="20" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-204" value="&lt;font style=&quot;font-size: 8px;&quot;&gt;0&lt;/font&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;" vertex="1" parent="Gxz8XZ3srZawtTpm0HoM-213">
          <mxGeometry x="3.125" y="55" width="30" height="25" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-205" value="&lt;font style=&quot;font-size: 8px;&quot;&gt;0&lt;/font&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;" vertex="1" parent="Gxz8XZ3srZawtTpm0HoM-213">
          <mxGeometry x="23.125" y="80" width="20" height="10" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-206" value="&lt;font style=&quot;font-size: 8px;&quot;&gt;1&lt;/font&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;" vertex="1" parent="Gxz8XZ3srZawtTpm0HoM-213">
          <mxGeometry x="113.125" y="80" width="20" height="10" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-207" value="" style="endArrow=none;html=1;rounded=0;fillColor=#f5f5f5;strokeColor=#666666;" edge="1" parent="Gxz8XZ3srZawtTpm0HoM-213">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="123.125" y="80" as="sourcePoint" />
            <mxPoint x="123.125" y="70" as="targetPoint" />
          </mxGeometry>
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-209" value="&lt;font style=&quot;font-size: 8px;&quot;&gt;Probability&lt;/font&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;rotation=-90;" vertex="1" parent="Gxz8XZ3srZawtTpm0HoM-213">
          <mxGeometry x="-15.315000000000055" y="37.19" width="45.63" height="15" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-210" value="&lt;font style=&quot;font-size: 8px;&quot;&gt;Proportion of tokens&lt;/font&gt;" style="text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;rotation=0;" vertex="1" parent="Gxz8XZ3srZawtTpm0HoM-213">
          <mxGeometry x="33.125" y="80" width="90" height="15" as="geometry" />
        </mxCell>
        <mxCell id="Gxz8XZ3srZawtTpm0HoM-212" value="" style="endArrow=none;html=1;exitX=1.009;exitY=0.602;exitDx=0;exitDy=0;exitPerimeter=0;curved=1;strokeColor=#82b366;fillColor=#d5e8d4;strokeWidth=2;" edge="1" parent="Gxz8XZ3srZawtTpm0HoM-213" source="Gxz8XZ3srZawtTpm0HoM-204">
          <mxGeometry width="50" height="50" relative="1" as="geometry">
            <mxPoint x="83.125" y="60" as="sourcePoint" />
            <mxPoint x="123.125" y="20" as="targetPoint" />
            <Array as="points">
              <mxPoint x="73.125" y="68" />
              <mxPoint x="83.125" y="40" />
              <mxPoint x="93.125" y="20" />
            </Array>
          </mxGeometry>
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
