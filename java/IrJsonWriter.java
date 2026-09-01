import java.lang.reflect.Field;
import java.lang.reflect.Modifier;
import java.util.*;

/**
 * Zero-dependency fast JSON serializer with NON_EMPTY collection filtering
 * to omit empty lists, empty maps, null values, and default false booleans.
 */
public class IrJsonWriter {

    public static String toJson(Object obj) {
        StringBuilder sb = new StringBuilder(64 * 1024);
        serialize(obj, sb, 0);
        return sb.toString();
    }

    @SuppressWarnings("unchecked")
    private static void serialize(Object obj, StringBuilder sb, int indent) {
        if (obj == null) {
            sb.append("null");
            return;
        }

        if (obj instanceof String) {
            sb.append(quote((String) obj));
        } else if (obj instanceof Number || obj instanceof Boolean) {
            sb.append(obj.toString());
        } else if (obj instanceof List) {
            List<?> list = (List<?>) obj;
            if (list.isEmpty()) {
                sb.append("[]");
                return;
            }
            sb.append("[\n");
            for (int i = 0; i < list.size(); i++) {
                indent(sb, indent + 1);
                serialize(list.get(i), sb, indent + 1);
                if (i < list.size() - 1) sb.append(",");
                sb.append("\n");
            }
            indent(sb, indent);
            sb.append("]");
        } else if (obj instanceof Map) {
            Map<String, ?> map = (Map<String, ?>) obj;
            if (map.isEmpty()) {
                sb.append("{}");
                return;
            }
            sb.append("{\n");
            int count = 0;
            int size = map.size();
            for (Map.Entry<String, ?> entry : map.entrySet()) {
                indent(sb, indent + 1);
                sb.append(quote(entry.getKey())).append(": ");
                serialize(entry.getValue(), sb, indent + 1);
                if (++count < size) sb.append(",");
                sb.append("\n");
            }
            indent(sb, indent);
            sb.append("}");
        } else {
            serializeObjectFields(obj, sb, indent);
        }
    }

    private static void serializeObjectFields(Object obj, StringBuilder sb, int indent) {
        Field[] fields = obj.getClass().getFields();
        sb.append("{\n");
        List<Field> nonNullFields = new ArrayList<>();
        for (Field f : fields) {
            if (Modifier.isTransient(f.getModifiers()) || Modifier.isStatic(f.getModifiers())) {
                continue;
            }
            try {
                Object val = f.get(obj);
                if (val == null) {
                    continue;
                }
                if (val instanceof Collection && ((Collection<?>) val).isEmpty()) {
                    continue; // Omit empty lists (e.g. indexedBy, conditions88, children, sourceFieldIds, targetFieldIds)
                }
                if (val instanceof Map && ((Map<?, ?>) val).isEmpty()) {
                    continue; // Omit empty maps
                }
                if (val instanceof Boolean && Boolean.FALSE.equals(val)) {
                    continue; // Omit default false booleans
                }
                nonNullFields.add(f);
            } catch (IllegalAccessException ignored) {}
        }

        for (int i = 0; i < nonNullFields.size(); i++) {
            Field f = nonNullFields.get(i);
            try {
                Object val = f.get(obj);
                indent(sb, indent + 1);
                sb.append(quote(f.getName())).append(": ");
                serialize(val, sb, indent + 1);
                if (i < nonNullFields.size() - 1) sb.append(",");
                sb.append("\n");
            } catch (IllegalAccessException ignored) {}
        }
        indent(sb, indent);
        sb.append("}");
    }

    private static void indent(StringBuilder sb, int level) {
        for (int i = 0; i < level; i++) {
            sb.append("  ");
        }
    }

    private static String quote(String str) {
        if (str == null) return "null";
        StringBuilder sb = new StringBuilder(str.length() + 16);
        sb.append('"');
        for (int i = 0; i < str.length(); i++) {
            char c = str.charAt(i);
            switch (c) {
                case '"': sb.append("\\\""); break;
                case '\\': sb.append("\\\\"); break;
                case '\b': sb.append("\\b"); break;
                case '\f': sb.append("\\f"); break;
                case '\n': sb.append("\\n"); break;
                case '\r': sb.append("\\r"); break;
                case '\t': sb.append("\\t"); break;
                default:
                    if (c < 32 || c >= 127) {
                        sb.append(String.format("\\u%04x", (int) c));
                    } else {
                        sb.append(c);
                    }
            }
        }
        sb.append('"');
        return sb.toString();
    }
}
