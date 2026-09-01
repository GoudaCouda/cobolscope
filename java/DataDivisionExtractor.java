import io.proleap.cobol.CobolParser.*;
import io.proleap.cobol.asg.metamodel.call.*;
import io.proleap.cobol.asg.metamodel.data.DataDivision;
import io.proleap.cobol.asg.metamodel.data.datadescription.*;
import io.proleap.cobol.asg.metamodel.data.file.FileDescriptionEntry;
import io.proleap.cobol.asg.metamodel.data.file.FileSection;
import io.proleap.cobol.asg.metamodel.data.linkage.LinkageSection;
import io.proleap.cobol.asg.metamodel.data.localstorage.LocalStorageSection;
import io.proleap.cobol.asg.metamodel.data.workingstorage.WorkingStorageSection;

import java.util.*;

/**
 * Extracts Data Division sections, builds field hierarchies, and computes exact memory layouts.
 */
public class DataDivisionExtractor {

    public static void extractDataDivision(
            DataDivision dataDiv,
            IrModel.DataDictionaryDto dict,
            Map<DataDescriptionEntry, String> entryToIdMap,
            Map<String, String> nameToIdMap) {

        if (dataDiv == null) return;

        // Working-Storage Section (Contiguous sequential memory offsets across 01 levels)
        WorkingStorageSection ws = dataDiv.getWorkingStorageSection();
        if (ws != null && ws.getRootDataDescriptionEntries() != null) {
            for (DataDescriptionEntry root : ws.getRootDataDescriptionEntries()) {
                IrModel.DataFieldDto f = mapDataField(root, null);
                if (f != null) dict.workingStorageSection.add(f);
            }
            computeMemoryLayout(dict.workingStorageSection, "WS", true, entryToIdMap, nameToIdMap);
        }

        // Linkage Section (Each 01 parameter has its own base offset 0)
        LinkageSection ls = dataDiv.getLinkageSection();
        if (ls != null && ls.getRootDataDescriptionEntries() != null) {
            for (DataDescriptionEntry root : ls.getRootDataDescriptionEntries()) {
                IrModel.DataFieldDto f = mapDataField(root, null);
                if (f != null) dict.linkageSection.add(f);
            }
            computeMemoryLayout(dict.linkageSection, "LK", false, entryToIdMap, nameToIdMap);
        }

        // Local-Storage Section (Contiguous stack memory offsets across 01 levels)
        LocalStorageSection lss = dataDiv.getLocalStorageSection();
        if (lss != null && lss.getRootDataDescriptionEntries() != null) {
            for (DataDescriptionEntry root : lss.getRootDataDescriptionEntries()) {
                IrModel.DataFieldDto f = mapDataField(root, null);
                if (f != null) dict.localStorageSection.add(f);
            }
            computeMemoryLayout(dict.localStorageSection, "LS", true, entryToIdMap, nameToIdMap);
        }

        // File Section (FDs and their records share the FD buffer starting at offset 0)
        FileSection fs = dataDiv.getFileSection();
        if (fs != null && fs.getFileDescriptionEntries() != null) {
            for (FileDescriptionEntry fd : fs.getFileDescriptionEntries()) {
                IrModel.FileDescriptionDto fdDto = new IrModel.FileDescriptionDto();
                fdDto.name = fd.getName();
                fdDto.location = new IrModel.SourceLocationDto(fd.getCtx());
                if (fd.getFileControlEntry() != null) {
                    fdDto.selectName = fd.getFileControlEntry().getName();
                }
                if (fd.getRootDataDescriptionEntries() != null) {
                    for (DataDescriptionEntry root : fd.getRootDataDescriptionEntries()) {
                        IrModel.DataFieldDto f = mapDataField(root, null);
                        if (f != null) fdDto.records.add(f);
                    }
                    computeMemoryLayout(fdDto.records, "FD_" + fd.getName().replaceAll("[^a-zA-Z0-9_-]", "_"), false, entryToIdMap, nameToIdMap);
                }
                dict.fileSection.add(fdDto);
            }
        }
    }

    public static IrModel.DataFieldDto mapDataField(DataDescriptionEntry entry, String parentUsage) {
        if (entry == null) return null;

        IrModel.DataFieldDto dto = new IrModel.DataFieldDto();
        dto.asgEntry = entry;
        dto.name = entry.getName() != null ? entry.getName() : "FILLER";
        dto.level = entry.getLevelNumber() != null ? entry.getLevelNumber() : 1;
        dto.location = new IrModel.SourceLocationDto(entry.getCtx());

        if (entry instanceof DataDescriptionEntryGroup) {
            DataDescriptionEntryGroup group = (DataDescriptionEntryGroup) entry;

            if (group.getPictureClause() != null) {
                dto.pic = group.getPictureClause().getPictureString();
            }
            if (group.getUsageClause() != null && group.getUsageClause().getUsageClauseType() != null) {
                dto.usage = group.getUsageClause().getUsageClauseType().name();
            } else if (parentUsage != null) {
                dto.usage = parentUsage;
            } else {
                dto.usage = "DISPLAY";
            }
            if (group.getValueClause() != null && group.getValueClause().getCtx() != null) {
                dto.value = CobolTextCleaner.cleanValue(CobolTextCleaner.cleanContextText(group.getValueClause().getCtx()));
            }
            if (group.getRedefinesClause() != null) {
                if (group.getRedefinesClause().getRedefinesCall() != null) {
                    dto.redefines = group.getRedefinesClause().getRedefinesCall().getName();
                } else if (group.getRedefinesClause().getCtx() != null) {
                    dto.redefines = CobolTextCleaner.cleanRedefines(CobolTextCleaner.cleanContextText(group.getRedefinesClause().getCtx()));
                }
            }
            if (group.getFiller() != null && group.getFiller()) {
                dto.isFiller = true;
            }
            if (group.getJustifiedClause() != null) {
                dto.isJustified = true;
            }
            if (group.getBlankWhenZeroClause() != null) {
                dto.isBlankWhenZero = true;
            }
            if (group.getSynchronizedClause() != null) {
                dto.isSynchronized = true;
            }

            // OCCURS clause
            if (group.getOccursClauses() != null && !group.getOccursClauses().isEmpty()) {
                OccursClause occurs = group.getOccursClauses().get(0);
                Integer fromVal = null;
                if (occurs.getFrom() != null && occurs.getFrom().getCtx() != null) {
                    try {
                        fromVal = Integer.parseInt(occurs.getFrom().getCtx().getText().trim());
                    } catch (NumberFormatException ignored) {}
                }
                Integer toVal = null;
                if (occurs.getTo() != null && occurs.getTo().getValue() != null) {
                    toVal = occurs.getTo().getValue().intValue();
                } else if (occurs.getTo() != null && occurs.getTo().getCtx() != null) {
                    try {
                        toVal = Integer.parseInt(occurs.getTo().getCtx().getText().trim());
                    } catch (NumberFormatException ignored) {}
                }

                if (toVal != null) {
                    dto.occursMin = fromVal;
                    dto.occursMax = toVal;
                } else if (fromVal != null) {
                    dto.occursMin = fromVal;
                    dto.occursMax = fromVal;
                }

                if (occurs.getOccursDepending() != null && occurs.getOccursDepending().getCtx() != null) {
                    dto.dependingOn = CobolTextCleaner.cleanDependingOn(CobolTextCleaner.cleanContextText(occurs.getOccursDepending().getCtx()));
                }
                if (occurs.getOccursIndexed() != null && occurs.getOccursIndexed().getIndices() != null) {
                    for (var indexCall : occurs.getOccursIndexed().getIndices()) {
                        if (indexCall.getName() != null) dto.indexedBy.add(indexCall.getName());
                    }
                }
            }

            // Children & Level 88 Conditions (propagating effective usage to children)
            if (group.getDataDescriptionEntries() != null) {
                for (DataDescriptionEntry child : group.getDataDescriptionEntries()) {
                    if (child.getLevelNumber() != null && child.getLevelNumber() == 88) {
                        IrModel.Condition88Dto c88 = mapCondition88(child);
                        if (c88 != null) dto.conditions88.add(c88);
                    } else {
                        IrModel.DataFieldDto childDto = mapDataField(child, dto.usage);
                        if (childDto != null) dto.children.add(childDto);
                    }
                }
            }
        } else if (entry instanceof DataDescriptionEntryCondition) {
            // Standalone condition
            IrModel.Condition88Dto c88 = mapCondition88(entry);
            if (c88 != null) dto.conditions88.add(c88);
        }

        return dto;
    }

    public static IrModel.Condition88Dto mapCondition88(DataDescriptionEntry entry) {
        IrModel.Condition88Dto c88 = new IrModel.Condition88Dto();
        c88.name = entry.getName();
        c88.location = new IrModel.SourceLocationDto(entry.getCtx());

        if (entry instanceof DataDescriptionEntryCondition) {
            DataDescriptionEntryCondition cond = (DataDescriptionEntryCondition) entry;
            if (cond.getValueClause() != null && cond.getValueClause().getValueIntervals() != null) {
                for (ValueInterval interval : cond.getValueClause().getValueIntervals()) {
                    if (interval.getCtx() != null) {
                        c88.values.add(CobolTextCleaner.cleanValue(CobolTextCleaner.cleanContextText(interval.getCtx())));
                    }
                }
            } else if (cond.getValueClause() != null && cond.getValueClause().getCtx() != null) {
                c88.values.add(CobolTextCleaner.cleanValue(CobolTextCleaner.cleanContextText(cond.getValueClause().getCtx())));
            }
        }
        return c88;
    }

    public static void computeMemoryLayout(
            List<IrModel.DataFieldDto> rootFields,
            String sectionPrefix,
            boolean sequentialRoots,
            Map<DataDescriptionEntry, String> entryToIdMap,
            Map<String, String> nameToIdMap) {

        Map<String, IrModel.DataFieldDto> nameMap = new LinkedHashMap<>();

        // Pass 1: Build paths, lengths, deterministic line-based IDs, and symbol index
        for (IrModel.DataFieldDto root : rootFields) {
            buildPathsAndLengths(root, sectionPrefix, null, nameMap, entryToIdMap, nameToIdMap);
        }

        // Pass 2: Calculate absolute and relative offsets
        int runningSectionOffset = 0;
        for (IrModel.DataFieldDto root : rootFields) {
            int rootBaseOffset = 0;
            if (root.redefines != null) {
                IrModel.DataFieldDto target = null;
                for (IrModel.DataFieldDto prev : rootFields) {
                    if (prev == root) break;
                    if (root.redefines.equalsIgnoreCase(prev.name)) {
                        target = prev;
                        break;
                    }
                }
                if (target == null && nameMap.containsKey(root.redefines.toUpperCase())) {
                    target = nameMap.get(root.redefines.toUpperCase());
                }
                if (target != null) {
                    rootBaseOffset = target.byteOffset;
                }
            } else if (sequentialRoots) {
                rootBaseOffset = runningSectionOffset;
            }

            calculateOffsets(root, rootBaseOffset, 0, nameMap);

            if (sequentialRoots) {
                if (root.redefines == null) {
                    runningSectionOffset += root.byteLength;
                } else {
                    int overlayEnd = rootBaseOffset + root.byteLength;
                    if (overlayEnd > runningSectionOffset) {
                        runningSectionOffset = overlayEnd;
                    }
                }
            }
        }
    }

    private static void buildPathsAndLengths(
            IrModel.DataFieldDto field,
            String sectionPrefix,
            String parentPath,
            Map<String, IrModel.DataFieldDto> nameMap,
            Map<DataDescriptionEntry, String> entryToIdMap,
            Map<String, String> nameToIdMap) {

        String path = parentPath == null ? field.name : parentPath + "." + field.name;
        field.qualifiedName = path;

        int line = field.location != null ? field.location.startLine : 0;
        String cleanName = field.name.replaceAll("[^a-zA-Z0-9_-]", "_");
        field.id = sectionPrefix + "_L" + line + "_" + cleanName;

        if (field.asgEntry != null && entryToIdMap != null) {
            entryToIdMap.put(field.asgEntry, field.id);
        }
        if (nameToIdMap != null && !Boolean.TRUE.equals(field.isFiller)) {
            if (!nameToIdMap.containsKey(field.name.toUpperCase())) {
                nameToIdMap.put(field.name.toUpperCase(), field.id);
            }
            nameToIdMap.put(path.toUpperCase(), field.id);
        }

        nameMap.put(field.name.toUpperCase(), field);
        nameMap.put(path.toUpperCase(), field);

        int multiplier = (field.occursMax != null && field.occursMax > 0) ? field.occursMax : 1;

        if (field.children.isEmpty()) {
            int elemBytes = calculateElementaryByteLength(field.pic, field.usage);
            field.byteLength = elemBytes * multiplier;
        } else {
            int totalGroupBytes = 0;
            for (IrModel.DataFieldDto child : field.children) {
                buildPathsAndLengths(child, sectionPrefix, path, nameMap, entryToIdMap, nameToIdMap);
                if (child.redefines == null) {
                    totalGroupBytes += child.byteLength;
                }
            }
            field.byteLength = totalGroupBytes * multiplier;
        }
    }

    private static void calculateOffsets(
            IrModel.DataFieldDto field,
            int absoluteOffset,
            int relativeOffset,
            Map<String, IrModel.DataFieldDto> nameMap) {

        field.byteOffset = absoluteOffset;
        field.relativeOffset = relativeOffset;

        int childRunningRelOffset = 0;
        for (IrModel.DataFieldDto child : field.children) {
            if (child.redefines != null) {
                IrModel.DataFieldDto target = null;
                for (IrModel.DataFieldDto sibling : field.children) {
                    if (sibling == child) break;
                    if (child.redefines.equalsIgnoreCase(sibling.name)) {
                        target = sibling;
                        break;
                    }
                }
                if (target == null && nameMap != null) {
                    String qTarget = (field.qualifiedName != null ? field.qualifiedName + "." : "") + child.redefines;
                    target = nameMap.get(qTarget.toUpperCase());
                    if (target == null) {
                        target = nameMap.get(child.redefines.toUpperCase());
                    }
                }
                if (target != null) {
                    calculateOffsets(child, target.byteOffset, target.relativeOffset, nameMap);
                    continue;
                }
            }

            int childAbs = absoluteOffset + childRunningRelOffset;
            int childRel = childRunningRelOffset;
            calculateOffsets(child, childAbs, childRel, nameMap);
            childRunningRelOffset += child.byteLength;
        }
    }

    public static int calculateElementaryByteLength(String pic, String usage) {
        String u = usage != null ? usage.toUpperCase().replace("-", "_") : "DISPLAY";

        if (pic == null || pic.trim().isEmpty()) {
            if ("POINTER".equals(u) || "INDEX".equals(u) || "PROCEDURE_POINTER".equals(u)) return 4;
            if ("COMP_1".equals(u)) return 4;
            if ("COMP_2".equals(u)) return 8;
            return 0;
        }

        String normalizedPic = expandPicRepetitions(pic.toUpperCase().trim());
        int totalDigits = countDigits(normalizedPic);
        int displayChars = countDisplayCharacters(normalizedPic);

        switch (u) {
            case "COMP":
            case "COMP_4":
            case "COMP_5":
            case "BINARY":
                if (totalDigits <= 4) return 2;
                if (totalDigits <= 9) return 4;
                return 8;

            case "COMP_3":
            case "PACKED_DECIMAL":
                return (totalDigits / 2) + 1;

            case "COMP_1":
                return 4;

            case "COMP_2":
                return 8;

            case "POINTER":
            case "INDEX":
            case "PROCEDURE_POINTER":
                return 4;

            case "DISPLAY":
            default:
                return displayChars > 0 ? displayChars : (totalDigits > 0 ? totalDigits : 1);
        }
    }

    public static String expandPicRepetitions(String pic) {
        if (pic == null) return "";
        StringBuilder sb = new StringBuilder();
        int i = 0;
        while (i < pic.length()) {
            char c = pic.charAt(i);
            if (c == '(') {
                int close = pic.indexOf(')', i);
                if (close != -1 && sb.length() > 0) {
                    String numStr = pic.substring(i + 1, close).trim();
                    char prevChar = sb.charAt(sb.length() - 1);
                    try {
                        int count = Integer.parseInt(numStr);
                        for (int k = 1; k < count; k++) {
                            sb.append(prevChar);
                        }
                    } catch (NumberFormatException ignored) {}
                    i = close + 1;
                    continue;
                }
            }
            sb.append(c);
            i++;
        }
        return sb.toString();
    }

    public static int countDigits(String normalizedPic) {
        int digits = 0;
        for (int i = 0; i < normalizedPic.length(); i++) {
            char c = normalizedPic.charAt(i);
            if (c == '9' || c == 'Z' || c == '*' || c == '+' || c == '-' || c == '$') {
                digits++;
            }
        }
        return digits;
    }

    public static int countDisplayCharacters(String normalizedPic) {
        int chars = 0;
        for (int i = 0; i < normalizedPic.length(); i++) {
            char c = normalizedPic.charAt(i);
            if (c == 'V' || c == 'S') {
                continue; // Virtual decimal or non-separate sign consumes 0 display bytes
            }
            if (c == 'C' && i + 1 < normalizedPic.length() && normalizedPic.charAt(i + 1) == 'R') {
                chars += 2;
                i++;
                continue;
            }
            if (c == 'D' && i + 1 < normalizedPic.length() && normalizedPic.charAt(i + 1) == 'B') {
                chars += 2;
                i++;
                continue;
            }
            chars++;
        }
        return chars;
    }
}
